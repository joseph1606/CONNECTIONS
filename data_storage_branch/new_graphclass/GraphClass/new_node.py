import json


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
