import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

import GraphClass.Joel.GraphClass as Graph
import GraphClass.Joel.EdgeClass as Edge
import GraphClass.Joel.NodeClass as Node
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


def Save(graph: Graph.Graph) -> CSV:
    pass


def Add(graph: Graph.Graph, csv) -> Graph.Graph:
    pass


def Filter(graph: Graph.Graph, params: str) -> Graph.Graph:
    pass


# skip shortestPath


def Merge(graph1: Graph.Graph, graph2: Graph.Graph) -> Graph.Graph:
    pass
