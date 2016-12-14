#Script takes in SCOPUS csv files which are lists of articles
#and creates article citation networks

import csv
from igraph import *

#tries to clean up article titles
def sanitize(text):
    text = text.replace(",", "")
    text = text.replace("\r", "")
    text = text.replace("\n", "")
    text = text.replace("\"", "")
    text = text.replace("'", "")
    text=text.lower()
    return text



#there is sometimes some garbage data in SCOPUS
#I suggest removing all arts with a title of less than 14
#also gets rid of general article names like "editorial"
cutoff=14

print "Creating a network from SCOPUS files"
print "Assumptions:
print "each infile is from a distinct journal"
print "each infile has a \"Title\" column and a \"References\" column"
print "Ignoring articles with titles of less than ", cutoff

print "Building node list"
G = Graph(directed=True)

headers = []

infiles = ["List of scopus files here"]

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

        
        if len(line["Title"])<cutoff:
            continue

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

print "Building edge list"

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

        if len(line["Title"])<cutoff:
            continue

        line["Title"] = sanitize(line["Title"])

        line["References"] = sanitize(line["References"])
        for node in VertexSeq(G):

            #edge goes from citing article to cited article
            if node["name"] in line["References"]:
                if not G.are_connected(line["Title"], node["name"]):#might already exist
                    G.add_edge(line["Title"], node["name"])

                
summary(G) 
#write out
G.write_gml("SCOPUS Network.gml")
