import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

import GraphClass.Joel.Graph as Graph
import GraphClass.Joel.Edge as Edge
import GraphClass.Joel.Node as Node
import GraphClass.Revaant.AuthorNode as Author
from GraphClass.Revaant.AuthorNode import AuthorNode


def CreateGraph(csv) -> Graph.Graph:
    pass


def Subgraph(graph: Graph.Graph, name: str) -> Graph.Graph:
    pass


# INTRODUCING A NEW FUNCTION
def Networkx(graph: Graph.Graph) -> nx.Graph:
    pass


def Vis(ntx: nx.Graph) -> Network:
    pass


def Save(graph: Graph.Graph) -> "csv":
    pass


def Add(graph: Graph.Graph, csv) -> Graph.Graph:
    pass


def Filter(graph: Graph.Graph, params: str) -> Graph.Graph:
    pass


# skip shortestPath


def Merge(graph1: Graph.Graph, graph2: Graph.Graph) -> Graph.Graph:
    pass
