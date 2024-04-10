import networkx as nx
import matplotlib.pyplot as plt
# from Functions import *
from parse import parseData
from SemanticScholarFuncs import *
# x = CreateGraph("connections3.csv")
# print("---------------------------------------------------------------------------")
# y = CreateGraph("connections.csv")

# z = MergeGraph(x,y)

#z = MergeGraph(x,y,[(a[0],b[0])])
# c = GetNodes(z)
# z.print_nodes()
#z.print_edges()
#z.print_relationships()

# m = Networkx(z)
#Vis(m)
#z.print_relationships()

#f.print_nodes()
#f.print_edges()
#f.print_relationships()

user_input = input("Enter a name: ")
#searchAuthor(user_input)
generate_author_dict(user_input)

