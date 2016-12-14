#take in the pickled community decomposition
#and the main graph
#output data for graphing at node and cluster level
#can be easily changed to work with different visualisations
#any graphics package can plot the network which results 

import igraph

print "Loading graph"
G = igraph.read("Network name here")
igraph.summary(G)
lg = G.layout_fruchterman_reingold()#choose layout algorithm

print "Loading communities"
import pickle
vc = pickle.load( open( "Clustering Results.p", "rb" ) )

#make a new cluster level graph, with layout
Gclustered = vc.cluster_graph(combine_edges="sum")
lc = Gclustered.layout_fruchterman_reingold()#choose layout algorithm

#add definitive cluster id to all nodes
for v in Gclustered.vs():
    Gclustered.vs[v.index]["clid"] = v.index

print "Outputting node level - nodes dataset"
output = open("VOXPOL - Node Dataset - for visualisation.csv", "w")
output.write("node id,community_id,community_size,name,xpos,ypos\n")

clid = 0

for cluster in vc:

    for node in cluster:

        x,y = l[node]
        output.write(str(node))
        output.write(",")
        output.write(str(Gsub.vs[node]['auto']))
        output.write(",")
        output.write(str(clid))
        output.write(",")
        output.write(str(len(cluster)))
        output.write(",")
        output.write(str(Gsub.vs[node]["name"]))
        output.write(",")
        output.write(str(x))
        output.write(",")
        output.write(str(y))
        output.write("\n")
        

    clid += 1

output.close()

print "Outputting node level - egdes dataset"
output = open("VOXPOL - Node-Edge Dataset - for visualisation.csv", "w")
output.write("source_id,target_id,sxpos,sypos,txpos,typos,weight\n")

for edge in G.es():
    s = edge.source
    t = edge.target

    sx,sy = l[s]
    tx,ty = l[t]

    output.write(str(s))
    output.write(",")
    output.write(str(t))
    output.write(",")
    output.write(str(sx))
    output.write(",")
    output.write(str(sy))
    output.write(",")
    output.write(str(tx))
    output.write(",")
    output.write(str(ty))
    output.write(",")
    output.write(str(edge["weight"]))
    output.write("\n")
        
output.close()


print "Outputting community level"

output = open("VOXPOL - Community Dataset - for visualisation.csv", "w")
output.write("community_id,community_size,xpos,ypos\n")

clid = 0
for cluster in vc:

    x,y = l[clid]

    output.write(str(clid))
    output.write(",")
    output.write(str(len(cluster)))
    output.write(",")
    output.write(str(x))
    output.write(",")
    output.write(str(y))
    output.write("\n")
        

    clid += 1

output.close()

output = open("VOXPOL - Community-Edge Dataset - for visualisation.csv", "w")
output.write("source_id,target_id,sxpos,sypos,txpos,typos,weight\n")

clid = 0
for edge in Gclustered.es():
    s = edge.source
    t = edge.target

    sx,sy = l[s]
    tx,ty = l[t]

    output.write(str(s))
    output.write(",")
    output.write(str(t))
    output.write(",")
    output.write(str(sx))
    output.write(",")
    output.write(str(sy))
    output.write(",")
    output.write(str(tx))
    output.write(",")
    output.write(str(ty))
    output.write(",")
    output.write(str(edge["weight"]))
    output.write("\n")
        

    clid += 1

output.close()

print "Doing top 10 clusters"
