import networkx as nx
import matplotlib.pyplot as plt
from GraphClass import Graph
from NodeClass import Node
from EdgeClass import Edge
from Functions import *

from parse import parseData

G = CreateGraph("connections2.csv")
print("------------------------------------------------------------------------------------------------------")
#G.print_nodes()
print("Edges:- ")
#G.print_relationships()
G.print_edges()


'''
print("********************************************************************************************")
x = SubGraph(G,"name1")
print("===============================================================================================")
x.print_nodes()

'''
