"""
We iterate through self.nodes to add all nodes into graph, then we iterate
through self.connections to connect all added nodes."""

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

import graphclass as Graph
import edgeclass as Edge
import nodeclass as Node
import author as Author
from author import AuthorNode
from author import PaperNode


# this takes the Graph Object with the associated ntx object, and just wraps it in pyvis
def Vis(ntx):
    nt = Network("500px", "500px")
    # fancy rendering here
    nt.from_nx(ntx)
    nt.toggle_physics(True)
    nt.show(
        "ntx.html", notebook=False
    )  # something between frontend/backend happens here for rendering, but this is the basics


def Networkx(graph):
    ntx = nx.Graph()

    # add nodes to networkx object
    for node_id, node in graph.nodes.items():

        title = titelize(node.attributes)

        if type(node) is AuthorNode:
            aliases = "Alisases: " + ", ".join(node.aliases) + "\n"
            papers = paper_string(node.papers)
            title = aliases + papers + title

        ntx.add_node(node_id, title=title, label=node.name)

    # add edges to networkx object
    for (node1_id, node2_id), edge_id in graph.connections.items():
        title = titelize(graph.edges[edge_id].relationships)
        ntx.add_edge(node1_id, node2_id, title=title)

    return ntx


# NEEDS TO TAKE CARE OF DIRECTED RELATIONSHIPS
def titelize(attributes: dict) -> str:
    title = ""

    # k should be String, v should be List
    for k, v in attributes.items():
        title += k + ": " + ", ".join(v) + "\n"

    return title


def paper_string(papers) -> str:
    title = ""

    for paper in papers:
        title += paper.title + ": " + paper.year + "\n"

    return title
