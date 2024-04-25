import networkx as nx
import matplotlib.pyplot as plt
from GraphClass import Graph
from NodeClass import Node
from EdgeClass import Edge
from Functions import *
from parse import parseData


def switch_tuple_elements(lst):
    return [(t[1], t[0]) for t in lst]

# Example usage:
my_list = [('apple', 'banana'), ('cat', 'dog'), ('sun', 'moon')]
result = switch_tuple_elements(my_list)
print(result)




