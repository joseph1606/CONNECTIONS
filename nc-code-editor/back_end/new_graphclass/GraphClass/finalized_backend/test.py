import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

graph = CreateGraph("connections3.csv")

# Vis(graph)
graph.print_directed()
# lamb = lambda node: True if "Connections" in node.attributes else False
# fg = FilterGraph(graph, None, lamb)
