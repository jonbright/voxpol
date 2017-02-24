###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017

#This file takes in data from an edge list csv file. Assumes this file has source, target and weight columns.

#To run, place this script in the same folder as your input data file
#Change the following to the name of your file
infile_name = "INPUT FILE1"
#the output will be a file entitled "VOXPOL Edge List Network.gml"

from igraph import *
import csv

#create graph
infile = open(infile_name, "r")
idgen = UniqueIdGenerator()
edgelist = []

for line in csv.DictReader(infile):
    edgelist.append((idgen[line["source"]], idgen[line["target"]], int(line["weight"])))

g = Graph()
g.add_vertices(len(idgen))
g.vs["name"] = idgen.values()
for source, target, weight in edgelist:
    g.add_edge(source, target, weight=weight)

infile.close()

g.write_gml("VOXPOL Edge List Network.gml")
