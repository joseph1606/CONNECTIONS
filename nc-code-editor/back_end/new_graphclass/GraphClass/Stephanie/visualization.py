"""
We iterate through self.nodes to add all nodes into graph, then we iterate
through self.connections to connect all added nodes."""

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

import GraphClass.Ely.graphclass as Graph
import GraphClass.Ely.edgeclass as Edge
import GraphClass.Ely.nodeclass as Node
import GraphClass.Ely.author as Author
from GraphClass.Ely.author import AuthorNode
from GraphClass.Ely.author import PaperNode


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
     #   if "" THOUGHT ABOUT PUTTING AN IF CHECKING IF DIRECTED but this wouldn't be in the title variable
        ntx.add_edge(node1_id, node2_id, title=title)

    return ntx


def titelize(attributes: dict) -> str:
    title = ""

    # k should be String, v should be List
    for k, v in attributes.items():
        if k == "DIRECTED":
            for inner_key, inner_value in v.items():
                title += inner_key + ": " + ", ".join(inner_value) + "\n"

        else:
            title += k + ": " + ", ".join(v) + "\n"

    return title


def paper_string(papers) -> str:
    title = ""

    for paper in papers:
        title += paper.title + ": " + paper.year + "\n"

    return title
