import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

graph = SemanticSearch("Lisa Kern", 3)

l = NodeFromGraph(graph, "Lissa Griffin")[0]
f = FilterGraph(graph, {"Coauthor": [l.papers[2]]})
Vis(f)
