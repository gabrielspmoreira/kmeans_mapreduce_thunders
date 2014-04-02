This is a Python implementation of K-Means clustering algorithm using the Map Reduce paradigm.
It is customized for processing of a thunders dataset extracted from STARNET (Sferics Timing And Ranging NETwork).

The STARNET Lightning detection network (http://www.zeus.iag.usp.br) is run by the University of São Paulo, Brazil,
at Laboratório de Sensoriamento Remoto de Tempestades STORM-T, Department of Atmospheric Sciences, IAG.

Under src/ folder are the mapper and reducer scripts that can be run on a Hadoop environment. There is also a script to run the Hadoop job on Amazon Elastic Map Reduce (run_kmeans_emr.py).

A detailed description of the problem and the implementation is available on http://workingsweng.com.br/2014/04/clusterizando-raios-com-hadoop-e-k-means-em-map-reduce/
