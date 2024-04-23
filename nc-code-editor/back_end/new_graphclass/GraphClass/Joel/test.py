import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import parseData
   
   
   
"""
Rev, Walter, college, umbc -> {college:umd}
Purtilo, Ely, DIRECTED, "Mentor/Mentee" -> {DIRECTED: (Mentor,Mentee)} -> 
"""  


x = CreateGraph("connections3.csv")

#x.print_directed()

y = GetNodes(x)

node = y[0]

z = SubGraph(x,node)


print("*****************************")


#z.print_nodes()

z.print_directed()

print("-----------------------------")




#z.print_nodes()