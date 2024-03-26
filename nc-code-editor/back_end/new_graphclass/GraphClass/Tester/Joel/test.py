import networkx as nx
import matplotlib.pyplot as plt
from Graph import Graph
from Node import Node
from Edge import Edge
from Functions import CreateGraph
from parse import parseData

G = CreateGraph("data_storage_branch/new_graphclass/connections.csv")
print("------------------------------------------------------------------------------------------------------")

for node_id,node in G.nodes.items():
    print("node name & attributes ")
    print(node.getName())
    print(node.getAttributes())
    print(node.getID())
    print(node.getAttributesLocation())
    print()
