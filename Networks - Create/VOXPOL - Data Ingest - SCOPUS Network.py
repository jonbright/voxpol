###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017

#This file takes in data from the SCOPUS platform and converts it into network format
#It assumes that each line in the input file is an article with both a title and a list of references

#To run, place this script in the same folder as your input data file
#Change the following to the name of your file, or list of files
#(data comes out of SCOPUS at the journal level, so it might be valuable to have a list)
infiles = ["List of scopus files here"]
#the output will be a file entitled "VOXPOL - SCOPUS Network.csv"

import csv
from igraph import *

#Utility function which tries to clean up article titles
def sanitize(text):
    text = text.replace(",", "")
    text = text.replace("\r", "")
    text = text.replace("\n", "")
    text = text.replace("\"", "")
    text = text.replace("'", "")
    text=text.lower()
    return text

print "Adding nodes to graph"
G = Graph(directed=True)

headers = []

for i, infile in enumerate(infiles):

    infile = infile.strip()
    print i, infile

    try:
        inhandle = csv.DictReader(open(infile, "rU"))
        headers = inhandle.fieldnames
    except IOError:
        print "File not found: ", infile
        continue

    for i, line in enumerate(inhandle):

        line["Title"] = sanitize(line["Title"])

        #check node doesn't already exist
        try:
            G.vs.find(name=line["Title"])
            continue
        except:#throws an excpetion if it doesn't exist
            pass

        #if it doesn't, add the node to the graph
        G.add_vertex(name=line["Title"], journal=infile)

summary(G)

print "Adding edges to graph"
for i, infile in enumerate(infiles):

    infile = infile.strip()
    print i, infile

    try:
        inhandle = csv.DictReader(open(infile, "rU"))
        headers = inhandle.fieldnames
    except IOError:
        print "File not found: ", infile
        continue

    for line in inhandle:

        line["Title"] = sanitize(line["Title"])
        line["References"] = sanitize(line["References"])

        #check if this article cites any other article in the dataset
        for node in VertexSeq(G):
            #edge goes from citing article to cited article
            if node["name"] in line["References"]:
                G.add_edge(line["Title"], node["name"])

                
summary(G) 
#write out
G.write_gml("VOXPOL SCOPUS Network.gml")
