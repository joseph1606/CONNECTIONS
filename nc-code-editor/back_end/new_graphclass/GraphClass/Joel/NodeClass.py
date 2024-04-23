class Node:
    def __init__(self, name: str, attributes: dict):

        self.id = id(self)
        self.name = name
        self.attributes = attributes # self.attributes = attributes  # {'institution': ['umd', 'yale', 'columbia']}
        #self.attributes_id = id(attributes)
        
        self.directed = {}
        
        """
        for joel node,
        self.directed["mentor"] = [Purtilo_node]
        
        for purtilo node,
        self.directed["mentee"] = [Joel_node]
        """

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getAttributes(self):
        return self.attributes

    def updateAttributes(self, attributes: dict):
        for key, value in attributes.items():

            # checks if key is present
            if key in self.attributes:
                # Convert both lists to sets to remove duplicates, then merge them and convert back to list
                merged_values = list(set(self.attributes[key]).union(set(value)))
                self.attributes[key] = merged_values
            else:
                # If the key doesn't exist, add it to the dictionary with the value
                self.attributes[key] = value
                
                
    #def updateDirected(self,other_node:Node, directed_rel:str):
    def addDirected(self,other_node, directed_rel:str):
        if directed_rel in self.directed:
           self.directed[directed_rel].append(other_node)
        else:
            self.directed[directed_rel] = [other_node] 
