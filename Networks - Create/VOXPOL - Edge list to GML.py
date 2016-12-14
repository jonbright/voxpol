#takes an edge list
#converts to gml quickly
#nb there is a function "read Ncol" in igraph to do this
#but it never worked for me

from igraph import *
import csv

#create graph
infile = open("VOXPOL - Edge List.csv", "r")
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

g.write_gml("Edge List Network.gml")
