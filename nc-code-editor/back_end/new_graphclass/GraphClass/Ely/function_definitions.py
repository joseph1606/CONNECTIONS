import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

import new_graphclass.GraphClass.finalized_backend.GraphClass as Graph
import new_graphclass.GraphClass.finalized_backend.EdgeClass as Edge
import new_graphclass.GraphClass.finalized_backend.NodeClass as Node
import new_graphclass.GraphClass.finalized_backend.AuthorNode as Author
from new_graphclass.GraphClass.finalized_backend.AuthorNode import AuthorNode


def CreateGraph(csv) -> Graph.Graph:
    pass


def SemanticSearch(author_name: str) -> None:
    pass


def Subgraph(graph: Graph.Graph, name: str) -> Graph.Graph:
    pass


# INTRODUCING A NEW FUNCTION
def Networkx(graph: Graph.Graph) -> nx.Graph:
    pass


def Vis(ntx: nx.Graph) -> Network:
    pass


def Save(graph: Graph.Graph) -> CSV:
    pass


def Add(graph: Graph.Graph, csv) -> Graph.Graph:
    pass


def Filter(graph: Graph.Graph, params: str) -> Graph.Graph:
    pass


# skip shortestPath


def Merge(graph1: Graph.Graph, graph2: Graph.Graph) -> Graph.Graph:
    pass
