import new_graphclass.GraphClass.new_node as new_node
from new_node import Node


class Edge:
    def __init__(self, node1: Node, node2: Node, relationships: dict = None):
        self.node1 = node1
        self.node2 = node2

        # relationships will be a dictinoary of relationship: relationship value pairings
        self.relationships = relationships
