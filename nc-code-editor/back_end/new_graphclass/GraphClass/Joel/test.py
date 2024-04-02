import networkx as nx
import matplotlib.pyplot as plt
from new_graphclass.GraphClass.finalized_backend.GraphClass import Graph
from new_graphclass.GraphClass.finalized_backend.NodeClass import Node
from new_graphclass.GraphClass.finalized_backend.EdgeClass import Edge
from new_graphclass.GraphClass.finalized_backend.Functions import *

from parse import parseData

G = CreateGraph(
    "/Users/elycohen/Desktop/College/Computer Science Classes/CMSC435/team_work/git_connections/new_connections/nc-code-editor/back_end/new_graphclass/GraphClass/Joel/connections.csv"
)
print(
    "------------------------------------------------------------------------------------------------------"
)
# G.print_nodes()
print("Edges:- ")
# G.print_relationships()
G.print_edges()


"""
print("********************************************************************************************")
x = SubGraph(G,"name1")
print("===============================================================================================")
x.print_nodes()

"""
