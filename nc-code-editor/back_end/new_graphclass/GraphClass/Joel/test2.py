import networkx as nx
import matplotlib.pyplot as plt
from GraphClass import Graph
from NodeClass import Node
from EdgeClass import Edge
from Functions import *
from parse import parseData



x = CreateGraph("connections3.csv")
list_of_nodes = x.get_nodes()

y = CreateGraph()
y = CreateGraph("connections4.csv")
#x.print_edges()
print("print node -------------------------------")
AddNodes(y,list_of_nodes)
z = SubGraph(x,list_of_nodes[0])
#z.print_nodes()
#print("print edges -------------------------------")
z.print_edges()
print("print relationships -------------------------------")
#y.print_relationships()


