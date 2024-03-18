import new_graphclass.GraphClass.new_node as new_node
from new_node import Node
import new_graphclass.GraphClass.new_edges as new_edges
from new_edges import Edge
import new_graphclass.GraphClass.new_author_node as new_author_node 
from new_author_node import Author 


import networkx as nx
'''
from pyvis.network import Network
import json_fix
import json
from libdatasources.SemanticScholar import SemanticScholar
from libdatasources.PatentView import PatentView
import random
from GraphClass import new_ID_Constants
from libdatasources.find_in_other_databases import bulk_lookup
from networkx.readwrite import json_graph
from lookup_forms import lookup_classes
'''

def compare_dates(date1, date2):
    if date2 is None or date1 is None:
        return False
    return date2 > date1

class Graph:
    def __init__(self):
        