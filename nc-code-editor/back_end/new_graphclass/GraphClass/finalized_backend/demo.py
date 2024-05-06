import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

ed_g = SemanticSearch("Ed Lazowska", 1)

pur_g = SemanticSearch("James Purtilo", 1)

col_list = Collision(ed_g, pur_g, True)
merged = MergeGraph(ed_g, pur_g, col_list)
# Vis(merged)
# for node in c2["R. Fatland"]:
#    print(node.name, node.aliases)
# Vis(merged)
# THIS IS NEW FOR DEMO

demo_g = CreateGraph("demo.csv")
col_list = Collision(demo_g, merged, True)
merged = MergeGraph(demo_g, merged, col_list)

Save(merged, "demo2.csv")

demo2 = CreateGraph("demo2.csv")
Vis(merged)
