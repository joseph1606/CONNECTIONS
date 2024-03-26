"""
import new_GraphClass as GC
from new_GraphClass import Graph
import new_node
from new_node import Node
import new_edges
from new_edges import Edge
import new_author_node as new_auth
from new_author_node import Author
from CSV_Parsing.parse import parseData
"""

from Graph import Graph
from Node import Node
from Edge import Edge
from parse import parseData


def CreateGraph(csv):
    G = Graph()

    (names1, names2, attributes) = parseData(csv)

    if names2 is None:
        for name, attribute in zip(names1, attributes):
            named_nodes = G.search_named_nodes(name)
            G.disambiguation(named_nodes,name,attribute)
            
            # no need to create an edge

    else:
        for name1, name2, attribute in zip(names1, names2, attributes):
            
            named_nodes1 = G.search_named_nodes(name1)
            named_nodes2 = G.search_named_nodes(name2)
            
            disambiguated_node1 = G.disambiguation(named_nodes1,name1,attribute)
            disambiguated_node2 = G.disambiguation(named_nodes2,name2,attribute)
                       
            # techincally if a new node was created in disambiguation there wouldnt need to check for edge
            edge = G.search_edge(disambiguated_node1,disambiguated_node2)
            
            # if there was an edge
            if edge:
                G.update_edge(edge,attribute)
                    
            else:
                G.add_edge(disambiguated_node1,disambiguated_node2,attribute)
                    
            
    return G

