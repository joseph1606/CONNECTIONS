import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

ed_g = SemanticSearch("Ed Lazowska", 1)

pur_g = SemanticSearch("Purtilo", 2)
# lamb = lambda node: True if "Connections" in node.attributes else False
# fg = FilterGraph(graph, None, lamb)
length = len(pur_g.nodes)
add = []
count = 0
for node_id, node in ed_g.nodes.items():
    if count < 8:
        add.append(node)
    count += 1

pur_g = AddNodes(pur_g, add)


def fun(node):
    if "Coauthor" in node.attributes:
        return True
    else:
        False


print(len(pur_g.nodes))

# pur_g.print_nodes()
pur_g = FilterGraph(pur_g, None, fun)

print(len(pur_g.nodes))

Vis(pur_g)
