#!/usr/bin/python

import sys, re, math

CLUSTERS_FILENAME = 'clusters.txt'

clusters = []
delta_clusters = dict()

def read_from_clusters_cache_file(clusters_file):
    f = open(clusters_file, 'r')
    data = f.read()
    f.close()
    del f
    return data

def read_clusters():
    cluster_data = read_from_clusters_cache_file(CLUSTERS_FILENAME)
    for line in cluster_data.strip().split("\n"):
        data = line.strip().split("\t")
        centroid_id, coords = data
        latitude, longitude = coords.strip().split(";")
        clusters.append((centroid_id, float(latitude), float(longitude)))
        delta_clusters[centroid_id] = (0, 0, 0)

def get_distance_coords(lat1, long1, lat2, long2):
	#Calculate euclidian distance between two coordinates
    dist = math.sqrt(math.pow(lat1 - lat2,2) + math.pow(long1 - long2,2))
    return dist

def get_nearest_cluster(latitude, longitude):
    nearest_cluster_id = None
    nearest_distance = 1000000000
    for cluster in clusters:
        dist = get_distance_coords(latitude, longitude, cluster[1], cluster[2])
        if dist < nearest_distance:
            nearest_cluster_id = cluster[0]
            nearest_distance = dist
    return nearest_cluster_id


read_clusters()

regexWords = re.compile("\s+")

for line in sys.stdin:
    line = line.strip()
    words = regexWords.split(line)
    if words == None or len(words) != 29:
        print "ERROR PARSING LINE (Columns: "+str(len(words))+") - ",line
        continue
    else:
        year, month, day, hour, minute, second, millisecond, latitude, longitude, major_ellipse_error, atd_error, quality_control, polarity,rx_employed, atd_pairs, rx1, rx2, rx3, rx4, rx5, rx6, rx7, rx8, rx9, rx10, rx11, rx12, rx13, rx14 = words
        latn = float(latitude)
        longn = float(longitude)
        nearest_cluster_id = get_nearest_cluster(latn, longn)
        sumy, sumx, cont = delta_clusters[nearest_cluster_id]
        delta_clusters[nearest_cluster_id] = (sumy+latn, sumx+longn, cont+1)
        
for key in delta_clusters:
    sumy, sumx, cont = delta_clusters[key]
    print key + "\t" + str(sumy)+";"+str(sumx)+";"+str(cont)

