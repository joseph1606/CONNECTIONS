import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

ed_g = SemanticSearch("Ed Lazowska", 1)
dav = SemanticSearch("John Zahorjan")

"""
pur_g = SemanticSearch("Purtilo", 2)
# lamb = lambda node: True if "Connections" in node.attributes else False
# fg = FilterGraph(graph, None, lamb)
length = len(pur_g.nodes)
add = []
count = 0
for node_id, node in ed_g.nodes.items():
    if count < 8:
        add.append(node)
        print(node.name)
        print(node.attributes)
    count += 1

pur_g = AddNodes(pur_g, add)
# 31 nodes in the combined graph now
# Vis(pur_g)


def fun(node):
    if "Coauthor" in node.attributes:
        return True
    else:
        False


# pur_g.print_nodes()
g = FilterGraph(pur_g, None, fun)
Vis(g)
"""
c = Collision(ed_g, dav)
col = []


for name, pair in c.items():
    col.append(pair)


m = MergeGraph(ed_g, dav, col)

Vis(m)
