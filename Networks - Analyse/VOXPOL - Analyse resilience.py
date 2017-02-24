###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017

#This file takes in a network in GML format
#It analyses the amount of nodes which have to be deleted for it to break up
#both random and targetted attacks are employed
#To run, place this script in the same folder as your input data file
#Change the following to the name of your file
infile_name = "INPUT FILE1"
#the output will be a file entitled "VOXPOL - Forum Resilience.csv"



from igraph import *
import random

g = read(infile_name)
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
