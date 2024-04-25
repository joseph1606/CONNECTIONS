from NodeClass import Node


class Edge:
    def __init__(self, node1: Node, node2: Node, attributes: dict = None):
        self.id = id(self)
        self.node1 = node1
        self.node2 = node2
        self.relationships = attributes  # {relationship : [relationship_values]}
        self.directed = []

    def getID(self):
        return self.id

    def getNode1(self):
        return self.node1

    def getNode2(self):
        return self.node2

    def getRelationships(self):
        return self.relationships

    def updateRelationships(self, attributes: dict):
        for key, value in attributes.items():

            # might change to below code tbh

            # checks if key is present
            # if key in self.attributes:
            # if value not in self.attributes[key]:
            # self.attributes[key].append(value)

            # else:
            # self.attributes[key] = value

            if key in self.relationships:
                # Convert both lists to sets to remove duplicates, then merge them and convert back to list
                merged_values = list(set(self.relationships[key]).union(set(value)))
                self.relationships[key] = merged_values
            else:
                # If the key doesn't exist, add it to the dictionary with the value
                self.relationships[key] = value

    def addDirected(self, directed_rel: tuple):
        if directed_rel not in self.directed:
            self.directed.append(directed_rel)

    def print_directed(self):
        print(self.node1.name)
        print(self.node2.name)
        print(self.directed)
