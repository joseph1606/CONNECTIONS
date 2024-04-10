import networkx as nx
import matplotlib.pyplot as plt

# from Functions import *
from parse import parseData
from SemanticScholarFuncs import *
from Functions import *

# x = CreateGraph("connections3.csv")
# print("---------------------------------------------------------------------------")
# y = CreateGraph("connections.csv")

# z = MergeGraph(x,y)

# z = MergeGraph(x,y,[(a[0],b[0])])
# c = GetNodes(z)
# z.print_nodes()
# z.print_edges()
# z.print_relationships()

# m = Networkx(z)
# Vis(m)
# z.print_relationships()

# f.print_nodes()
# f.print_edges()
# f.print_relationships()

g = CreateGraph("./connections.csv")
f = CreateGraph("./connections3.csv")

m = MergeGraph(g, f)
# n = Networkx(m)
# Vis(n)

node = nodeFromGraph(m, "James")

sub = SubGraph(m, node[0])

n = Networkx(sub)

Vis(n)

# Vis(n)
# x = makeAuthor(user_input,1,5)
# print_author_details(x)
# generate_author_dict(user_input,1)
