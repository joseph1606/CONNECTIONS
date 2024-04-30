import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

first = CreateGraph("practice1.csv")
second = CreateGraph("practice2.csv")

c = Collision(first, second)
print(c)
m = MergeGraph(first, second, CollisionList(c))
Vis(m)
