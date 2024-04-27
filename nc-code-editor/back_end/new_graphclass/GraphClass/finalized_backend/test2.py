import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

graph = CreateGraph("connections3.csv")


def fun(node):
    if "Age" in node.attributes:
        return True
    else:
        return False


# Vis(graph)
graph = FilterGraph(graph, None, fun)

pjr = NodeFromGraph(graph, "pjr")[0]
Vis(graph)
