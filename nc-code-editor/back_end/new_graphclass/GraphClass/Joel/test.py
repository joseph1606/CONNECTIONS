import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import parseData
   
x = CreateGraph("connections3.csv")
print("---------------------------------------------------------------------------")
y = CreateGraph("connections.csv")

a = GetNodes(x)
b = GetNodes(y)


z = MergeGraph(x,y)

#z = MergeGraph(x,y,[(a[0],b[0])])
c = GetNodes(z)
z.print_nodes()
#z.print_edges()
#z.print_relationships()

m = Networkx(z)
#Vis(m)
#z.print_relationships()



#f.print_nodes()
#f.print_edges()
#f.print_relationships()
