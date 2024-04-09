import networkx as nx
from timeit import timeit

# import matplotlib.pyplot as plt
from Functions import *


# import new_graphclass.GraphClass.finalized_backend.GraphClass

# from parse import parseData


G = CreateGraph(
    "/Users/elycohen/Desktop/College/Computer Science Classes/CMSC435/team_work/git_connections/new_connections/nc-code-editor/back_end/new_graphclass/GraphClass/Ely/example_csv.csv"
)

g_nx = Networkx(G)

Vis(g_nx)


"""
time = timeit(
    lambda: vis(g_nx),
    number=1,
)

print(time)"""


"""
print(
    "------------------------------------------------------------------------------------------------------"
)
G.print_nodes()
print("Edges:- ")
# G.print_relationships()
G.print_edges()
"""

"""
print("********************************************************************************************")
x = SubGraph(G,"name1")
print("===============================================================================================")
x.print_nodes()

"""
