class Node:
    def __init__(self, name: str, attributes: dict = None):

        self.id = id(self)
        self.name = name
        # self.attributes = attributes  # {'institution': ['umd', 'yale', 'columbia']}
        # Create a deep copy of the original dictionary if attributes are provided
        # self.attributes = copy.deepcopy(attributes) if attributes else {}
        self.attributes = attributes  # self.attributes = attributes  # {'institution': ['umd', 'yale', 'columbia']}
        # self.attributes_id = id(attributes)

        self.directed = {}

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getAttributes(self):
        return self.attributes

    # def getAttributesLocation(self):
    # return self.attributes_id

    # attributes = {str:list[str]}
    # {'institution': ['umd', 'yale', 'columbia']}
    def updateAttributes(self, attributes: dict):
        for key, value in attributes.items():

            # might change to below code tbh

            # checks if key is present
            # if key in self.attributes:
            # if value not in self.attributes[key]:
            # self.attributes[key].append(value)

            # else:
            # self.attributes[key] = value

            # checks if key is present
            if key in self.attributes:
                # Convert both lists to sets to remove duplicates, then merge them and convert back to list
                merged_values = list(set(self.attributes[key]).union(set(value)))
                self.attributes[key] = merged_values
            else:
                # If the key doesn't exist, add it to the dictionary with the value
                self.attributes[key] = value

    # def updateDirected(self,other_node:Node, directed_rel:str):
    def addDirected(self, other_node, directed_rel: str):

        if other_node in self.directed:
            if directed_rel not in self.directed[other_node]:
                self.directed[other_node].append(directed_rel)

        else:
            self.directed[other_node] = [directed_rel]

    def print_directed(self):
        print("===================")
        print("Node name is: ")
        print(self.name)
        print()
        for node, rel_value in self.directed.items():
            print("Other node and its values are: ")
            print(node.name)
            print(rel_value)
            print()
