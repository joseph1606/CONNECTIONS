"""
We iterate through self.nodes to add all nodes into graph, then we iterate
through self.connections to connect all added nodes."""

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

import GraphClass.Joel.Graph as Graph
import GraphClass.Joel.Edge as Edge
import GraphClass.Joel.Node as Node
import GraphClass.Revaant.AuthorNode as Author
from GraphClass.Revaant.AuthorNode import AuthorNode 


#this takes the Graph Object with the associated ntx object, and just wraps it in pyvis 
def vis(ntx): 
    nt = Network("500px", "500px")
    #fancy rendering here
    nt.from_nx(ntx)
    return nt #something between frontend/backend happens here, but this is the basics 
    
    
#this takes the Graph Object, goes through dictionaries    
def filter(graph, relationships="all"):
    ntx = nx.Graph()
    
    for n in graph.nodes:
        #add them and parameters into ntx graph 
        #we'll have node.id as the primary identifier, and then i'll 
        #make according paramters for data, like name=node.name 
        #going to need to have a type check for if the node is an AuthorNode 
        if n is type AuthorNode: 
        
        else: 
            
        
    for (node1, node2, edge) in self.connections: 
        #add edges accordingly, using the edge primary identifer as edge.id 
        
        
    return ntx #return networkx object 