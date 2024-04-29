import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

graph = CreateGraph("practice1.csv")
nba = CreateGraph("nba.csv")
Vis(nba)
