#!/usr/bin/python
import sys, time, uuid, math, datetime, random, boto.emr

BUCKET_NAME = 'raios-starnet' #Replace with your bucket on S3
DATA_PATH = 'data_2014_02_28/' #Folder where data is on your S3 bucket
MAPPER_SCRIPT_PATH = 'mapper_kmeans.py' #Path to the mapper script on your S3 bucket
REDUCER_SCRIPT_PATH = 'reducer_kmeans.py' #Path to the reducer script on your S3 bucket
LOGS_PATH = '/logs_kmeans' #Path where the EMR logs will be generated on your S3 bucket
AWS_ACCESS_KEY = 'XPTO' #Replace with your AWS ACCESS KEY
AWS_SECRET_KEY = 'XPTO' #Replace with your AWS SECRET KEY
AWS_REGION = 'sa-east-1' #Replace with your region
CLUSTERS_FILENAME = 'clusters.txt' #File name of the clusters file that will be generated after each map reduce step

INSTANCE_TYPE = 'm1.small' #EC2 Instance size - BE AWARE OF AMAZON COSTS!
NUM_INSTANCES = 10 #Number of instances running the EMR job  BE AWARE OF AMAZON COSTS!

REGION_EXTENT = (6.3,-74.5,-35.2,-31.9) #Upper-left and Bottom-Right coords for Brazilian extent, for clusters random initialization
CLUSTERS_NUMBER = 10 #Number of clusters to be positioned by K-Means

#Creates connections on Amazon EMR and S3 services
connEmr = boto.emr.connect_to_region(AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
connS3 = boto.connect_s3(AWS_ACCESS_KEY,AWS_SECRET_KEY)

def get_new_output_job_path():
    return 'output/kmeans_'+str(uuid.uuid1()).replace('-','_')+"/"

#Merges the results of reducers tasks (part-00000, part-00001 files)	
def get_merged_job_result(bucket, output_job_path):
    final_content = ""
    b = connS3.get_bucket(bucket)
    for key in b.list(output_job_path):
        k = boto.s3.key.Key(b)
        k.key = key.name
        part_content = k.get_contents_as_string()
        k.close(True)
        final_content = final_content + part_content
    return final_content

def write_to_s3_file(bucket, keyname, data):
    b = connS3.get_bucket(bucket)
    k_write = boto.s3.key.Key(b)
    k_write.key = keyname
    k_write.set_contents_from_string(data)
    k_write.close(True)

def read_from_s3_file(bucket, keyname):
    b = connS3.get_bucket(bucket)
    k = botos.s3.key.Key(b)
    k.key = keyname
    result = k.get_contents_as_string()
    k.close(True)
    return result

def get_random_coords_in_region():
    latitude = random.uniform(REGION_EXTENT[2], REGION_EXTENT[0])
    longitude = random.uniform(REGION_EXTENT[1], REGION_EXTENT[3])
    return latitude, longitude

def get_random_initial_clusters(clusters_number):
    clusters = []
    for k in range(clusters_number):
        latitude, longitude = get_random_coords_in_region()
        clusters.append(str(k)+"\t"+str(latitude)+";"+str(longitude))
    return clusters

def generate_initial_clusters_on_s3(clusters_number, output_job_path):    
    initial_clusters_file_path = "/"+output_job_path+CLUSTERS_FILENAME
    print "Generating initial random clusters (",str(clusters_number),") at ", initial_clusters_file_path
    clusters = get_random_initial_clusters(clusters_number)
    write_to_s3_file(BUCKET_NAME, initial_clusters_file_path, "\n".join(clusters))
    return initial_clusters_file_path

def get_distance_coords(lat1, long1, lat2, long2):
    dist = math.sqrt(math.pow(lat1 - lat2,2) + math.pow(long1 - long2,2))
    return dist

def get_clusters_from_text(clusters_text):
    clusters = dict()
    for line in clusters_text.strip().split("\n"):
        data = line.strip().split("\t")
        centroid_id, coords = data
        latitude, longitude = coords.strip().split(";")
        clusters[centroid_id] = (float(latitude), float(longitude))
    return clusters

def get_delta_clusters_coords(step_result, previous_result):    
    clusters1 = get_clusters_from_text(step_result)
    clusters2 = get_clusters_from_text(previous_result)
    total_dist = 0
    for key in clusters1:
        cluster1 = clusters1[key]
        cluster2 = clusters2[key]
        dist = get_distance_coords(cluster1[0], cluster1[1], cluster2[0], cluster2[1])
        total_dist += dist
    return total_dist

def upload_file_to_s3(local_file, bucket, keyname):
    f = open(local_file, 'r')
    data = f.read()
    f.close()
    del f
    write_to_s3_file(bucket, keyname, data)

def upload_mr_scripts():
    print "Uploading map and reduce script to bucket ",BUCKET_NAME
    upload_file_to_s3(MAPPER_SCRIPT_PATH, BUCKET_NAME, MAPPER_SCRIPT_PATH)
    upload_file_to_s3(REDUCER_SCRIPT_PATH, BUCKET_NAME, REDUCER_SCRIPT_PATH)

previous_step_result = ""
step_delta = 10000000
iteraction_count = 0
jobid = ""
job_state = ""

start_time=datetime.datetime.now()

output_job_path = get_new_output_job_path()

clusters_file_path = generate_initial_clusters_on_s3(CLUSTERS_NUMBER, output_job_path)

upload_mr_scripts()

print "Starting", NUM_INSTANCES, INSTANCE_TYPE, "instances"

try:
    while step_delta > 0.5:
        iteraction_count += 1
        print '-------------------------------------------'
        print 'ITERATION '+str(iteraction_count) 
        output_job_path_step = output_job_path+'Step'+str(iteraction_count)+'/'   

        print "Job step output path: " + output_job_path_step 

        step = boto.emr.step.StreamingStep(name='Kmeans EMR Step '+str(iteraction_count),
                              mapper='s3://'+BUCKET_NAME+'/'+MAPPER_SCRIPT_PATH,
                              reducer='s3://'+BUCKET_NAME+'/'+REDUCER_SCRIPT_PATH,
                              input='s3://'+BUCKET_NAME+'/'+DATA_PATH,
                              output='s3://'+BUCKET_NAME+'/'+output_job_path_step,
                              cache_files=['s3://'+BUCKET_NAME+clusters_file_path+'#'+CLUSTERS_FILENAME])

        if iteraction_count == 1:
            jobid = connEmr.run_jobflow(name='Kmeans EMR Job',
                                      log_uri='s3://'+BUCKET_NAME+LOGS_PATH,
                                      steps=[step],
                                      master_instance_type = INSTANCE_TYPE,
                                      slave_instance_type = INSTANCE_TYPE,
                                      num_instances = NUM_INSTANCES,
                                      keep_alive=True,
                                      action_on_failure='TERMINATE_JOB_FLOW')
        else:
            connEmr.add_jobflow_steps(jobid, step)

        while True:
            time.sleep(20)
            job_describe = connEmr.describe_jobflow(jobid)
            job_state = job_describe.state
            print time.strftime("%d/%m/%y %H:%M:%S", time.localtime()), " - JobId=", jobid, " - State=", job_state
            if job_state == u'COMPLETED' or job_state == u'FAILED' or job_state == u'WAITING' or job_state == u'TERMINATED': # (NOT STARTING, RUNNING OR SHUTTING_DOWN)
                print 'Step '+str(iteraction_count)+' Finished - Job Status: '+job_state   
                break            

        if job_state == u'FAILED':
            print "The Step Failed. Terminating Job..."
            print "Reason: ",job_describe.laststatechangereason
            sys.exit(1)

        clusters_file_path = "/"+output_job_path_step+CLUSTERS_FILENAME
        print "Merging results"
        step_result = get_merged_job_result(BUCKET_NAME, output_job_path_step)

	    print step_result

        if step_result == "":
            print "Erro - Step did not return any result"
            sys.exit(1)

        print "Saving merged results to: "+clusters_file_path
        write_to_s3_file(BUCKET_NAME, clusters_file_path, step_result)

        if previous_step_result != "":
            step_delta = get_delta_clusters_coords(step_result, previous_step_result)
            print "Delta Coods: ", step_delta

        previous_step_result = step_result

    end_time=datetime.datetime.now()
    ellapsed_time=(end_time-start_time).seconds
    print 'JOB FINISHED IN '+str(ellapsed_time)+' SECONDS'
    print 'FINAL CLUSTERS AVAILABLE AT '+clusters_file_path
finally:
    if jobid != "":
        "Terminating job and EC2 instances"
        connEmr.terminate_jobflow(jobid)
    print "Job Terminated"
