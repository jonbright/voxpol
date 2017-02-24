###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017

#This file takes in a network in GML format
#It runs a community detection algorithm, outputting the results as a pickled object for later use
#It analyses the amount of nodes which have to be deleted for it to break up
#NB It is worth separating community detection from further analysis (and pickling results)
#because many community detection algorithms may be stochastic
infile_name = "INPUT FILE1"
#the output will be a file entitled "VOXPOL Clustering Results.p"


import igraph

print "Reading graph"
G = igraph.read(infile_name)
igraph.summary(G)

#focus on giant component, weakly connected
Gsub = Gsub.clusters(mode="weak").giant()

print "Getting communities"
#the community detection algorithm can be modified here
#see http://igraph.org/python/doc/igraph.Graph-class.html for more options
vc = Gsub.community_infomap()

#freeze the clustering for later use
#this is useful as there is some clustering algorithms
#are non-deterministic
print "Outputting"
import pickle
pickle.dump(vc, open("VOXPOL Clustering Results.p", "wb" ))

