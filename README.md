This is a Python implementation of K-Means clustering algorithm using the Map Reduce paradigm.
It is customized for processing a thunders dataset, extracted from STARNET (Sferics Timing And Ranging NETwork) - http://www.zeus.iag.usp.br.

Under **src/** folder are the mapper and reducer scripts that can be run on a Hadoop environment. There is also a script to run the Hadoop job on Amazon Elastic Map Reduce (run_kmeans_emr.py).
Under **data/** folder is a sample of the thunders that "falled" on February 28, 2014.

A detailed description of the problem and this implementation is available on http://workingsweng.com.br/2014/04/clusterizando-raios-com-hadoop-e-k-means-em-map-reduce/
