# voxpol
Repository for network analysis tools developed during the voxpol project. These tools were developed during the course of a variety of ongoing research projects. In this repository I have attempted to generalise them a little in the hope that they migth be of use / inspiration to social science researchers who are starting to get to grips with network analysis in python using igraph.  

There are two types of file:

- In the networks - create folder are scripts which can be used to parse various types of input into a network structure. Three main types of input are tackled in particular: Twitter data (VOXPOL - Twitter Network.py), data from SCOPUS (VOXPOL - SCOPUS Network.py) and forum data which was collected during the course of the VOXPOL project (VOXPOL - Forum Network.py). The scopus file outputs directly to GML, on the assumption that a SCOPUS network won't be that big. The Twitter and forum data scripts output node and edge lists, which can be converted to GML also with the script provided. 

- In the networks - analyse folder are scripts which can be used to perform various types of analytical task. In particular, the sccripts enable the identification of communities, the labelling of these communities, outputting datasets which can then be graphed using GGPLOT2, and also analysing the resilience of forums. All of these scripts are based on the python-igraph package. They assume a GML input. 

Development of the scripts was supported by the VOXPOL project (http://www.voxpol.eu/), an EU FP7 funded academic network.  
