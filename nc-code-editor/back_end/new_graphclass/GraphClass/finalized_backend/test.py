import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *


x = CreateGraph(
    "new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/connections3.csv"
)
y = CreateGraph(
    "new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/connections.csv"
)
z = MergeGraph(x, y)

saveData(
    x.get_nodes(),
    "new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/test1.csv",
)
saveData(
    y.get_nodes(),
    "new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/test2.csv",
)
saveData(
    z.get_nodes(),
    "new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/test3.csv",
)

a = CreateGraph(
    "new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/test1.csv"
)
b = CreateGraph(
    "new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/test2.csv"
)
c = CreateGraph(
    "new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/test3.csv"
)

# a = x, b = y, c = z
# visualization seems to be broken, temp test code is commented below


"""
a.print_nodes()
print("``````````")
x.print_nodes()
print("~~~~~~")
a.print_edges()
print("``````````")
x.print_edges()
print("~~~~~~")
a.print_relationships()
print("``````````")
x.print_relationships()
print("---------------------------------------------------------------------------")

b.print_nodes()
print("``````````")
y.print_nodes()
print("~~~~~~")
b.print_edges()
print("``````````")
y.print_edges()
print("~~~~~~")
b.print_relationships()
print("``````````")
y.print_relationships()
print("---------------------------------------------------------------------------")

c.print_nodes()
print("``````````")
z.print_nodes()
print("~~~~~~")
c.print_edges()
print("``````````")
z.print_edges()
print("~~~~~~")
c.print_relationships()
print("``````````")
z.print_relationships()
print("---------------------------------------------------------------------------")

"""


# x = CreateGraph("connections3.csv")
# print("---------------------------------------------------------------------------")
# y = CreateGraph("connections.csv")

# z = MergeGraph(x,y)

# z = MergeGraph(x,y,[(a[0],b[0])])
# c = GetNodes(z)
# z.print_nodes()
# z.print_edges()
# z.print_relationships()

# m = Networkx(z)
# Vis(m)
# z.print_relationships()

# f.print_nodes()
# f.print_edges()
# f.print_relationships()

# user_input = "James Purtilo"
# searchAuthor(user_input)
# x = makeAuthor(user_input,1,5)
# print_author_details(x)
# generate_author_dict(user_input,1)



s = SemanticSearch("Jim Purtilo",1,2)

saveData(
    s.get_nodes(),
    "nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/test4.csv",
)

v = CreateGraph(
    "nc-code-editor/back_end/new_graphclass/GraphClass/finalized_backend/test4.csv"
)