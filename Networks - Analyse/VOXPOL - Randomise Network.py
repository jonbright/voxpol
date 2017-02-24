###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017

#This file takes in any GML file, and calculates 
infile_name = "INFILE_NAME"
#choose how many random runs of the network you would like. must be at least 2
limit = 100
#a list of functions you would like to apply each time
func_list = ["clust_coef", "apl"]

#here we define a series of functions which report statistics of interest
#there are two example ones here, more could be defined
#the important thing is that they take in a graph and return a metric
def clust_coef(g):
    return g.transitivity_undirected()

def apl(g):
    return g.average_path_length()



#utility functions
def mean(data):
    return sum(data)/float(len(n)) 

def ss(data):
    c = mean(data)
    return sum((x-c)**2 for x in data)

def sd(data):
    n = len(data)
    var = ss(data)/float(n)
    return var**0.5


#imports
from igraph import *
import random

print "Reading graph"
g = read(infile_name)

#initialise stats counter
stats = {}
for func in func_list:
    stats[func] = []

#now do random shuffles
print "Randomizing"
for i in range(0,limit):
    print i,
    #randomly rewire, preserving degree sequence
    #need to take weights out and put them back in
    weights = cnet.es["weight"]
    cnet.rewire(n=100)
    cnet.es["weight"] = weights
    print "Shuffled"

    #apply each function
    for func in func_list:
        stats[func].append(globals()[func]())

print "Output"
outfile = open("VOXPOL - Random trial results - " + limit + " trials.csv", "w")

#header
for func in func_list:
    outfile.write(func + " Mean")
    outfile.write(";")
    outfile.write(func + " SD")
    outfile.write(";")
outfile.write("\n")

    
for func in func_list:
    outfile.write(mean(stats[func]))
    outfile.write(";")
    outfile.write(sd(stats[func]))
    outfile.write(";")
outfile.write("\n")
    
