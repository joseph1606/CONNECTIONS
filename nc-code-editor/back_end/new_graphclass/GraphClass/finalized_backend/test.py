import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

graph = CreateGraph("joel.csv")

for node_id, node in graph.nodes.items():
    print(node.name, node.attributes)

lamb = lambda node: True if "Connections" in node.attributes else False
# fg = FilterGraph(graph, None, lamb)
