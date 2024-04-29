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
# THIS IS NEW FOR DEMO
demo_g = CreateGraph("demo.csv")
col_list = Collision(demo_g, merged, True)

merged = MergeGraph(demo_g, merged, col_list)

Vis(merged)
ed = NodeFromGraph(merged, "Edward D. Lazowska")
fbi = NodeFromGraph(merged, "FBI")

sp = ShortestPath(ed, fbi, merged)

sp_g = AddNodes(CreateGraph(), sp)
# Vis(sp_g)
