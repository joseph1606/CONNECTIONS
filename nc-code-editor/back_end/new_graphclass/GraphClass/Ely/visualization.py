"""
We iterate through self.nodes to add all nodes into graph, then we iterate
through self.connections to connect all added nodes."""

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

import GraphClass.Joel.GraphClass as Graph
import GraphClass.Joel.EdgeClass as Edge
import GraphClass.Joel.NodeClass as Node
import GraphClass.Revaant.AuthorNode as Author
from GraphClass.Revaant.AuthorNode import AuthorNode


# this takes the Graph Object with the associated ntx object, and just wraps it in pyvis
def Vis(ntx):
    nt = Network("500px", "500px")
    # fancy rendering here
    nt.from_nx(ntx)
    nt.show(
        "ntx.html"
    )  # something between frontend/backend happens here for rendering, but this is the basics


def Networkx(graph):
    ntx = nx.Graph()

    for node_id, node in graph.nodes.items():
        if type(node) is AuthorNode:
            pass
        else: 
            ntx.add_node(node_id, ......)
        
    return ntx
