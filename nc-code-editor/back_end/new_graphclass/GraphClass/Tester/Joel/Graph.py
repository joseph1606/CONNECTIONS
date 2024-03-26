import networkx as nx
from Node import Node
from Edge import Edge
import time

class Graph:
    def __init__(self):
        self.nxGraph = nx.MultiGraph(selfloops=False, multiedges=True)
        self.nodes = {}  # {node.id: node object}
        self.edges = {} # {edge.id:edge object}
        self.connections = {}  # {(node1.id, node2.id) : edge.id}
        
    def return_nxGraph(self):
        return self.nxGraph

    # assumes new node is to be added
    def add_node(self, name: str, attributes: dict):
        node = Node(name, attributes)
        self.nodes[node.getID()] = node
        print("Creating new node:", node.getName())
        print("Node attributes:", node.getAttributes())
        return node

    def add_edge(self, node1: Node, node2: Node, attributes: dict):
        edge = Edge(node1, node2, attributes)
        self.edges[edge.getID()] = edge
        self.connections[(node1.getID(), node2.getID())] = edge.getID()
        
    # might change later; so keeping it here for now
    def update_node(self, node:Node, attributes: dict):
        print("Updating node:",node.getName())
        print("Node id:",node.getID())
        node.updateAttributes(attributes)
        node.printAttributesLocation()
        return node
    
    # might change later; so keeping it here for now
    def update_edge(self, edge:Edge, attributes: dict):
        edge.updateRelationships(attributes)
        return edge

    # returns a dict (subdict of nodes) with the same name inputted
    def search_named_nodes(self, name: str):
        named_nodes = {}
        for node_id, node in self.nodes.items():
            if name == node.getName():
                named_nodes[node_id] = node
        return named_nodes

    # checks for edges; returns edge if found
    def search_edge(self, node1: Node, node2: Node):
        edge = None

        for ((node1_id, node2_id), edge_id) in self.connections.items():
            if (node1_id == node1.getID() and node2_id == node2.getID()) or (node1_id == node2.getID() and node2_id == node1.getID()):
                edge = self.edges[edge_id]
                break

        return edge


    # first attempts for solving disambiguity
    # named_nodes are nodes with the inputted name
    # returns 0 if a new node was created
    # returns 1 if a node was updated
    
    def disambiguation(self, named_nodes: dict, name: str, attributes: dict):
        if not named_nodes:
            # If there are no nodes with the provided name, create a new node
            new_node = self.add_node(name, attributes)
            return new_node
        
        print("+++++++++++++++++++++++++++++++++++++++++++")
        for i, (node_id, node) in enumerate(named_nodes.items(), start=1):
            
            print(f"{i}. {name}")
            print(f"{node.getAttributes()}")
            print()

        # Set choice to the index of the last node
        last_number = len(named_nodes) + 1

   
        # Ask the user to choose a node or create a new one
        while True:
            try:
                choice = int(input(f"Enter the number of the node you want or {last_number} to create a new one: "))
                if choice < 1 or choice > last_number:
                    raise ValueError
                break

            except ValueError:
                print("Invalid input. Please enter a valid number.")

        if choice == last_number:
            # Create a new node
            # Assuming attributes for the new node are provided by the user
            new_node = self.add_node(name, attributes)
            return new_node
        
        else:
            # Get the chosen node
            chosen_node = list(named_nodes.values())[choice - 1]
            chosen_node.updateAttributes(attributes)
            

            chosen_node.updateAttributes(attributes)

            
            # Now you can use the chosen_node as needed
            print("You chose: ", chosen_node.getName())
            print("with attributes: ", chosen_node.getAttributes())
            print()
            return chosen_node
    