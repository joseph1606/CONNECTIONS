import networkx as nx
import matplotlib.pyplot as plt
from GraphClass import Graph
from NodeClass import Node
from EdgeClass import Edge
from Functions import *

from parse import parseData
   
x = CreateGraph("connections3.csv")
print("---------------------------------------------------------------------------")
y = CreateGraph("connections4.csv")

a = GetNodes(x)
b = GetNodes(y)


z = MergeGraph(x,y,[(a[0],b[0]), (a[1],b[4]), (a[3],b[1])])

#z = MergeGraph(x,y,[(a[0],b[0])])
c = GetNodes(z)
#z.print_nodes()
#z.print_edges()
#z.print_relationships()
p = SubGraph(z,c[7])
dic = {}
dic["CollEge"] = ["UMD"]
#z.print_relationships()
print(format_dict(dic))

f = FilterGraph(z,dic)
d = GetNodes(f)



#f.print_nodes()
#f.print_edges()
#f.print_relationships()
