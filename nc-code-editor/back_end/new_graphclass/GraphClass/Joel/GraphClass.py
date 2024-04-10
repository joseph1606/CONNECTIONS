import networkx as nx
from NodeClass import Node
from EdgeClass import Edge
from AuthorNode import AuthorNode
import copy
import colorsys

class Graph:
    def __init__(self):
        self.nodes = {}  # {node.id: node object}
        self.edges = {}  # {edge.id:edge object}
        self.connections = {}  # {(node1.id, node2.id) : edge.id}
        self.relationships = {}
        self.directed = {}
        self.colors = {}

        """
        
        self.relationships = {
           "Institution": {
               "UMD": [...] #all nodes with “Institution” relationship, “UMD” value 
               "Yale": [...]
           },
           
           "Age": {
               "21": [...] #all nodes with “Age” relationship, “21” value -> NOT A LIST OF NODE IDS, A LIST OF NODES (references)
               "34": [...]
           }
           
           "Paper": {
               "PaperNode": [.....] #ALL AUTHOR NODES 
               "PaperNode2": [...]
           }
           
           "directed":{
               "(mentor,mentee)": [(Purtilo,Ely),(Purtilo,Joel)]
           }
     
        }
        
        self.directed = {
        
               "(mentor,mentee)": [(Purtilo,Ely),(Purtilo,Joel)]

        }
        """

    def return_nxGraph(self):
        return self.nxGraph

    # assumes new node is to be added
    def add_node(self, name: str, attributes: dict):
        attributes = copy.deepcopy(attributes)
        node = Node(name, attributes)
        self.nodes[node.getID()] = node
        return node

    # updates a existing node
    def update_node(self, node: Node, attributes: dict):
        attributes = copy.deepcopy(attributes)
        node.updateAttributes(attributes)
        return node
    
    # adds a Semantic Scholar Node to graph
    def add_ssnode(self,name:str,attributes:dict,aliases, authorId, url, papers=None):
        attributes = copy.deepcopy(attributes)
        ssnode = AuthorNode(name,attributes,aliases,authorId,url,papers)
        self.nodes[ssnode.getID()] = ssnode
        return ssnode

    # adds a new edge
    def add_edge(self, node1: Node, node2: Node, attributes: dict):
        attributes = copy.deepcopy(attributes)
        edge = Edge(node1, node2, attributes)
        self.edges[edge.getID()] = edge
        self.connections[(node1.getID(), node2.getID())] = edge.getID()
        return edge

    # might change later; so keeping it here for now
    def update_edge(self, edge: Edge, attributes: dict):
        attributes = copy.deepcopy(attributes)
        edge.updateRelationships(attributes)
        return edge

    # returns list of nodes ids that have the same attribute type and corresponding value -> which is use to create/update edges
    # also updates relationships dict
    def relationship_nodes(self, node: Node, attribute_type: str, attribute_value: str):
        relationship_nodes = []
        #node_id = node.getID()
        
        """
        self.relationships = {
           "Institution": {
               "UMD": [...] #all nodes (ids) with “Institution” relationship, “UMD” value 
               "Yale": [...]
           }
        }
        """

        # eg check to see if institution is present
        if attribute_type in self.relationships:

            # eg check to see if UMD is present
            if attribute_value in self.relationships[attribute_type]:

                # to avoid dups; could also switch to sets?
                if node not in self.relationships[attribute_type][attribute_value]:

                    # return list of other nodes with same attribute type and value; to be use to create/update edges
                    relationship_nodes = self.relationships[attribute_type][attribute_value]
                    # update relationships
                    self.relationships[attribute_type][attribute_value].append(node)

                # dont need else cuz then the node associated with that particular attribute type and attribute value
                # is already present in relationships and has the corresponding edges

            # if UMD is not present, relationships needs to be updated
            else:
                self.relationships[attribute_type][attribute_value] = [node]

        # if institution isnt present need to add it to dict
        else:
            temp_dict = {}
            # before adding institution we need to add umd
            temp_dict[attribute_value] = [node]
            self.relationships[attribute_type] = temp_dict

        # print("****************************************")
        # print(relationship_nodes)
        return relationship_nodes

    # returns a list of nodes that have the inputted name
    def search_named_nodes(self, name: str):
        named_nodes = []
        for node_id, node in self.nodes.items():
            if name == node.getName():
                named_nodes.append(node)
        return named_nodes

    # checks for edges; returns list of edge objects if found
    def search_edge(self, node1: Node, node2: Node = None):
        edge_objects = []

        if node2 is None:
            # If only one node is provided, search for edges connected to that node
            for (n1_id, n2_id), edge_id in self.connections.items():
                if node1.getID() in (n1_id, n2_id):
                    edge_objects.append(self.edges[edge_id])
        else:
            # If two nodes are provided, search for the edge between those nodes
            for (n1_id, n2_id), edge_id in self.connections.items():
                if (n1_id == node1.getID() and n2_id == node2.getID()) or (
                    n1_id == node2.getID() and n2_id == node1.getID()
                ):
                    edge_objects.append(self.edges[edge_id])
                    break

        return edge_objects

    def get_node(self, node_id: int):
        if node_id in self.nodes:
            return self.nodes[node_id]
        else:
            return None

    # returns a list of all nodes in the graph
    def get_nodes(self):
        nodes = []
        for node_id, node in self.nodes.items():
            nodes.append(node)
        return nodes

    # returns nodes dict
    def get_nodes_dict(self):
        return self.nodes

    def get_relationships(self):
        return self.relationships

    def print_nodes(self):
        for node in self.nodes.values():
            print()
            print(node.getName())
            print(node.getID())
            print(node.getAttributes())

    def print_edges(self):
        print()
        for edge in self.edges.values():
            print("Edge info: ")
            # print(edge.getNode1().getID())
            print(edge.getNode1().getName())
            print(edge.getNode1().getID())
            # print(edge.getNode2().getID())
            print(edge.getNode2().getName())
            print(edge.getNode2().getID())

            print(edge.getRelationships())
            print()

    def print_relationships(self):
        for relationship, nodes in self.relationships.items():
            print("=======================")
            print(f"{relationship}:")

            for value, associated_nodes in nodes.items():
                print(f"{value}:")
                for node in associated_nodes:
                    # print(f"{node_id}")
                    print(f"{node.getName()}")
                print()

    def generateColors(self):
        hue = 0
        saturation = 0.8
        value = 0.8

        for k in self.relationships.keys():
            hue += 0.618033988749895
            hue %= 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            r_int = int(r * 255)
            g_int = int(g * 255)
            b_int = int(b * 255)

            self.colors[k] = (r_int, g_int, b_int)

"""
    # first attempt for solving disambiguity
    # named_nodes is the list of nodes with the inputted name
    # returns the node object created/updated
    # NOT NEEDED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def disambiguation(self, named_nodes: list, name: str, attributes: dict):
        if not named_nodes:
            # If there are no nodes with the provided name, create a new node
            new_node = self.add_node(name, attributes)
            return new_node

        print("+++++++++++++++++++++++++++++++++++++++++++")
        for i, node in enumerate(named_nodes, start=1):
            print(f"{i}. {name}")
            print(f"{node.getAttributes()}")
            print()

        last_number = len(named_nodes)

        # Ask the user to choose a node or create a new one
        while True:
            choice = input(
                f"Enter the number of the node you want or 0 to create a new one: "
            )
            if choice.isdigit() and 0 <= int(choice) <= last_number:
                choice = int(choice)
                break
            print("Invalid input. Please enter a valid number.")

        if choice == 0:
            # Create a new node
            # Assuming attributes for the new node are provided by the user
            new_node = self.add_node(name, attributes)
            return new_node

        else:
            # Get the chosen node
            chosen_node = named_nodes[choice - 1]
            chosen_node.updateAttributes(attributes)

            # Now you can use the chosen_node as needed
            print("You chose: ", chosen_node.getName())
            print("with attributes: ", chosen_node.getAttributes())
            print()
            return chosen_node









"""
