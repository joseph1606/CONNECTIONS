import networkx as nx
import matplotlib.pyplot as plt
from GraphClass import Graph
from NodeClass import Node
from EdgeClass import Edge
from Functions import *

from parse import parseData
   
x = CreateGraph("connections4.csv")
print("---------------------------------------------------------------------------")
y = CreateGraph("connections3.csv")

a = GetNodes(x)
b = GetNodes(y)
print(a[4].getName())
print(b[4].getName())
z = MergeGraph(x,y,[(a[2],b[3]), (a[4],b[4])])


z.print_nodes()
#z.print_edges()
#z.print_relationships()