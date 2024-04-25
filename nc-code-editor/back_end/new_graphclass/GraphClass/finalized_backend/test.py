import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

graph = CreateGraph("joel.csv")

f = FilterGraph(graph, {"Age": [21, 22]})

lamb = lambda node: True if "Connections" in node.attributes else False
# fg = FilterGraph(graph, None, lamb)
