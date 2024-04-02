from Node import Node

class Edge:
    def __init__(self, node1: Node, node2: Node, attributes: dict = None):
        self.id = id(self)
        self.node1 = node1
        self.node2 = node2
        self.relationships = attributes # {relationship : [relationship_values]}

            
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
            if key in self.relationships:
                # Convert both lists to sets to remove duplicates, then merge them and convert back to list
                merged_values = list(set(self.relationships[key]).union(set(value)))
                self.relationships[key] = merged_values
            else:
                # If the key doesn't exist, add it to the dictionary with the value
                self.relationships[key] = value

                    
        #self.relationship[key] = self.relationship.get(key, []) + [values]
        
        