import networkx as nx
import matplotlib.pyplot as plt


class Person:
    def __init__(self, name):
        self.name = name
        self.id = id(self)


class Edge:
    def __init__(self, type):
        self.type = type
        self.id = id(self)


p = Person("ely")
d = Person("Mom")
e = Edge("parent/child")
G = nx.MultiGraph()

# G.add_node(p.id, name=p.name)
G.add_node(d.id, name=d.name)
G.add_edge(p.id, d.id, label=e.type)

G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'


nx.draw(G, with_labels=True, labels={p.id: p.name}, font_weight="bold")
plt.show()
