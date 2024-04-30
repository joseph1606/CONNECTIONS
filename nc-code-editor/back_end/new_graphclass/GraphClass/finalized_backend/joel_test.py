import networkx as nx
import matplotlib.pyplot as plt
from Functions import *
from parse import *
from SemanticScholarFuncs import *

g = CreateGraph("nba.csv")


g.print_edges()