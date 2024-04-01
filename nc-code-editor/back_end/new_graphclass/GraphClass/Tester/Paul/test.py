import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


class Graph:
    def __init__(self, nodes: dict, edges: dict):
        self.nxGraph = nx.MultiGraph(selfloops=False, multiedges=True)

        self.nodes = nodes
        self.edges = edges

class Node:
    def __init__(
        self,
        name: str,
        relationships: dict = None,
    ):

        self.id = id(self)
        self.name = name

        # relationships will be a dictionary of relationship: relationship value pairings
        self.relationships = relationships

    def getName(self):
        return self.name

    def rel_exist(self, relation):
        return True if relation in self.relationships else False

    def getRel(self, relation):
        return self.relationships[relation] if self.rel_exist(relation) else None
    
    def getString(self):
        return f"Name: {self.name}\nId: {self.id}"


class Edge:
    def __init__(self, node1: Node, node2: Node, relationships: dict = None):
        self.node1 = node1
        self.node2 = node2
        self.id = id(self)

        # relationships will be a dictinoary of relationship: relationship value pairings
        self.relationships = relationships


ely = Node("ely")
mom = Node("Mom")
paul = Node("paul")
edge1 = Edge(ely, mom, {"parent/child": "mother/son"})
edge2 = Edge(ely, paul, {"University": "UMD"})
graph = Graph({ely.id: ely, mom.id: mom, paul.id: paul} , {edge1.id: edge1, edge2.id: edge2})
nxGraph = nx.Graph()


def addEdge(graph, edge):
    graph.add_edge(edge.node1.getString(), edge.node2.getString(), label=edge.id)

for e in graph.edges:
    addEdge(nxGraph, graph.edges[e])


nx.draw(nxGraph, with_labels=True, font_weight="bold")


nx.draw_networkx_edge_labels(nxGraph, pos=nx.spring_layout(nxGraph))


nt = Network("500px", "500px")
nt.from_nx(nxGraph)
plt.show()
#nt.show("nx.html")

