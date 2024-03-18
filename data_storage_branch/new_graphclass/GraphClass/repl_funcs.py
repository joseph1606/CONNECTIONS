import new_GraphClass as GC
from new_GraphClass import Graph
import new_node
from new_node import Node
import new_edges
from new_edges import Edge
import new_author_node as new_auth
from new_author_node import Author
from CSV_Parsing.parse import parseData


def CreateGraph(csv):
    nodes, edges = parseData(csv)  # aux function for parsing
    new_Graph = Graph(nodes, edges)
    return new_Graph


def subGraph(graph, name):
    pass


def vis(graph):
    pass


def save(graph):
    pass


def add(graph, csv):
    nodes, edges = parseData(csv)
    pass


def filter(graph, attr_types, attr_values):
    pass


def shortestpath(graph, start_attr, end_attr):
    pass


def merge(graph1, graph2):
    pass
