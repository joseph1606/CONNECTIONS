class Node:
    def __init__(self, name: str, attributes: dict = None):

        self.id = id(self)
        self.name = name
        # self.attributes = attributes  # {'institution': ['umd', 'yale', 'columbia']}
        # Create a deep copy of the original dictionary if attributes are provided
        # self.attributes = copy.deepcopy(attributes) if attributes else {}
        self.attributes = attributes
        # self.attributes_id = id(attributes)

        # shallow copy
        # self.attributes = dict(attributes) if attributes else {}

    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name

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
