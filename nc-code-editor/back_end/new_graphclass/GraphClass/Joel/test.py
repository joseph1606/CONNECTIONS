import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import parseData
     
"""
Rev, Walter, college, umbc -> {college:umd}
Purtilo, Ely, DIRECTED, "Mentor/Mentee" -> {DIRECTED: (Mentor,Mentee)} -> 



print("printing graph.directed")    
g.print_directed()

print("Directed nodes")
for node in b:
    if node.directed:
        node.print_directed()
        print()


print()
print("Directed edges: ========================")
for edge_id,edge in g.edges.items():
    edge.print_directed()
    print()


    
        

"""  

g = CreateGraph("connections3.csv")

b = GetNodes(g)

subg = SubGraph(g,b[0])
y = GetNodes(subg)
    
    
g.print_edges()


    




