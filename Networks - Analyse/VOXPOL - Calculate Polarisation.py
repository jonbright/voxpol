###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017

#This script calculates Krackhardt and Stern's E-I index, a measure of polarisation in the network
#The index is based on two pairs of "seed nodes" and the communities around them
#This measure is similar to the one used in: https://arxiv.org/abs/1609.05003

#insert the name of the network file
infile_name = "network_file_name"

#insert the names of the nodes you wish to calculate for here
a, b = ("seed_a_name", "seed_b_name")

#imports
from igraph import *

#calculate E-I for a given pair of nodes
def calc_pair(g, a, b):

    #get ids
    id_a = g.vs.find(name=a).index
    id_b = g.vs.find(name=b).index

    #find all nodes with a connection to the central parties node
    nodes_a = g.neighbors(id_a, mode="IN")
    nodes_b = g.neighbors(id_b, mode="IN")

    #add central party node itself to the list
    nodes_a.append(id_a)
    nodes_b.append(id_b)

    #find boundary nodes
    a_to_b = g.es.select(_source_in = nodes_a, _target_in = nodes_b)
    b_to_a = g.es.select(_source_in = nodes_b, _target_in = nodes_a)
    boundary_a = [e.source for e in a_to_b]
    boundary_b = [e.source for e in b_to_a]
    boundary = list(set(boundary_a + boundary_b))#remove duplicates
    bound_len = len(boundary)

    #now get finalised internal nodes
    internal_nodes_a = [v for v in nodes_a if v not in boundary]
    internal_nodes_b = [v for v in nodes_b if v not in boundary]
    
    #count internal edges
    internal_a = len(g.es.select(_within = internal_nodes_a))
    internal_b = len(g.es.select(_within = internal_nodes_b))

    #count external edges
    a_to_b = len(g.es.select(_source_in = boundary, _target_in = party_nodes_b))
    b_to_a = len(g.es.select(_source_in = boundary, _target_in = party_nodes_a))
    external = a_to_b + b_to_a

    #versions of ei
    try:
        internal_e_tot = internal_a + internal_b
        ei = (external - internal_e_tot) / float(external + internal_e_tot)
    except ZeroDivisionError:
        ei = "ZeroDivErr"

    data_dict = {
        "internal_nodes_a":len(internal_nodes_a),
        "internal_nodes_b":len(internal_nodes_b),
        "boundary_nodes":bound_len,
        "internal_edges_a":internal_a,
        "internal_edges_b":internal_b,
        "external_edges_a":a_to_b,
        "external_edges_b":b_to_a,
        "external_edges":external,
        "ei":ei
        }

    return data_dict

print "Reading graph"
g = read(infile_name)
print "Calculating EI for the pair: " + str((a,b))
print calc_pair(g,a,b)

