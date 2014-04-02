#!/usr/bin/python

import sys, random

REGION_EXTENT = (6.3,-74.5,-35.2,-31.9) #Upper-left and Bottom-Right coords for Brazilian extent

valid_clusters = []

#Gets a random coordinate for Brazilian extent
def get_random_coords_in_region():
    latitude = random.uniform(REGION_EXTENT[2], REGION_EXTENT[0])
    longitude = random.uniform(REGION_EXTENT[1], REGION_EXTENT[3])
    return latitude, longitude

#When a cluster has no point associated, this function suggests a new coordinate for it, 
#based on existing clusters or generating a random coordinate
def suggest_valid_coords_to_cluster():
    valid_clusters_count = len(valid_clusters)
    if valid_clusters_count <= 1:  
        # Taking random values for a new coordinate      
        new_lat, new_long = get_random_coords_in_region()
    else:
        # Taking two clusters and positioning this on their average
        cid1 = random.randint(0, valid_clusters_count-1)
        cid2 = random.randint(0, valid_clusters_count-1)
        while cid1 == cid2:
            cid2 = random.randint(0, valid_clusters_count-1)

        cluster1 = valid_clusters[cid1]
        cluster2 = valid_clusters[cid2]
        new_lat = (cluster1[1] + cluster2[1]) / 2
        new_long = (cluster1[2] + cluster2[2]) / 2
    return new_lat, new_long

def emit_new_lat_long(cluster_id, sumy_total, sumx_total, count_total):
    if count_total == 0: #if the cluster did not attracted any point, change to a new coord        
        new_lat, new_long = suggest_valid_coords_to_cluster()
        return
    else:
        new_lat = sumy_total / count_total 
        new_long = sumx_total / count_total
        valid_clusters.append((cluster_id, new_lat, new_long))
    print cluster_id + "\t" + str(new_lat)+";"+str(new_long)

oldKey = None
sumy_total = 0
sumx_total = 0
count_total = 0

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    cluster_id, totals = data_mapped
    sumy, sumx, count = totals.strip().split(";")

    if oldKey and oldKey != cluster_id:        
        emit_new_lat_long(oldKey, sumy_total, sumx_total, count_total)
        sumy_total = 0
        sumx_total = 0
        count_total = 0

    oldKey = cluster_id
    sumy_total += float(sumy)
    sumx_total += float(sumx)
    count_total += float(count)

if oldKey != None:
    emit_new_lat_long(oldKey, sumy_total, sumx_total, count_total)
