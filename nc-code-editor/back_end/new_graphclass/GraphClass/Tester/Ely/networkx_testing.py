import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


class Person:
    def __init__(self, name):
        self.name = name
        self.id = id(self)


class Edge:
    def __init__(self, type):
        self.type = type
        self.id = id(self)


ely = Person("ely")
mom = Person("Mom")
edge = Edge("parent/child")
G = nx.Graph()

# G.add_node(p.id, name=p.name)
G.add_edge(ely, mom, cnx=edge)
# G.add_edge(ely, 1)


# create labels for dictionary
def generate_label(node):
    if isinstance(node, Person):
        return node.name
    else:
        return ""


def to_json(graph):
    graph_dict = {}

    for node in graph:
        print(node)
        graph_dict[node.id] = graph.name

    return graph_dict


# create a labels dictionary to pass as a parameter
labels = {node_id: generate_label(node_id) for node_id in G.nodes}


# nx.draw(G, with_labels=True, labels=labels, font_weight="bold")

edge_objects = nx.get_edge_attributes(G, "cnx")
edge_labels = {}

for k, v in edge_objects.items():
    edge_labels[k] = v.type

# print(edge_labels)
# nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G), edge_labels=edge_labels)
# plt.show()

graph_dict = to_json(G)
nt = Network("500px", "500px")
# populates the nodes and edges data structures
nt.from_nx(graph_dict)
# nt.show("nx.html")
