#takes in a gml network
#analyses the amount of nodes which have to be deleted for it to break up
#both random and targetted attacks are employed

from igraph import *
import random

g = read("network name here")
ran = g.copy()
num_nodes = g.vcount()

output = open("VOXPOL - Forum Resilience.csv", "w")
output.write("Num Deleted,Num Components - Targeted Attack,\
              Num Components - Random Attack\n")
i=0

#initial values
c = len(g.components(mode=WEAK))
cr = len(ran.components(mode=WEAK))

output.write(str(i))
output.write(",")
output.write(str(c))
output.write(",")
output.write(str(cr))
output.write("\n")

#delete all nodes eventually
while(i<num_nodes):

    i+=1

    #delete max betweenness node
    betlist = g.betweenness()
    max_value = max(betlist)
    max_index = betlist.index(max_value)
    g.delete_vertices(max_index)
    c = len(g.components(mode=WEAK))

    #delete random node
    ran.delete_vertices(random.choice(ran.vs()).index)
    cr = len(ran.components(mode=WEAK))

    output.write(str(i))
    output.write(",")
    output.write(str(c))
    output.write(",")
    output.write(str(cr))
    output.write("\n")

output.close()
