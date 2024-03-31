import networkx as nx
import matplotlib.pyplot as plt
from Graph import Graph
from Node import Node
from Edge import Edge
from Functions import *

from parse import parseData

G = CreateGraph("data_storage_branch/new_graphclass/connections.csv")
print("------------------------------------------------------------------------------------------------------")
G.print_nodes()


'''
print("********************************************************************************************")
x = SubGraph(G,"name1")
print("===============================================================================================")
x.print_nodes()

'''
