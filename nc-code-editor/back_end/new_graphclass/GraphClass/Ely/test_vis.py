import networkx as nx

# import matplotlib.pyplot as plt
# from GraphClass.Joel.GraphClass import Graph
# from GraphClass.Joel.NodeClass import Node
# from GraphClass.Joel.EdgeClass import Edge
from functions import *
from visualization import *

# from parse import parseData

G = CreateGraph(
    "/Users/elycohen/Desktop/College/Computer Science Classes/CMSC435/team_work/git_connections/new_connections/nc-code-editor/back_end/new_graphclass/GraphClass/Joel/connections.csv"
)

g_nx = Networkx(G)


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
