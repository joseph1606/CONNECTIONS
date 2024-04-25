import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import parseData
   
   
   
"""
Rev, Walter, college, umbc -> {college:umd}
Purtilo, Ely, DIRECTED, "Mentor/Mentee" -> {DIRECTED: (Mentor,Mentee)} -> 
"""  


g = CreateGraph("connections3.csv")

b = GetNodes(g)

subg = SubGraph(g,b[0])
y = GetNodes(subg)
    
print("printing graph.directed")    
subg.print_directed()
    
print("Directed nodes")
for node in y:
    node.print_directed()
    print()

print("Directed edges: ========================")
for edge_id,edge in subg.edges.items():
    edge.print_directed()
    print()
        




