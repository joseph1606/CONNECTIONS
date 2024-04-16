import networkx as nx
from Node import Node
from Edge import Edge

# Now most of the functions return the id of the node/edge created/updated

class Graph:
    def __init__(self):
        self.nxGraph = nx.MultiGraph(selfloops=False, multiedges=True)
        self.nodes = {}  # {node.id: node object}
        self.edges = {}  # {edge.id:edge object}
        self.connections = {}  # {(node1.id, node2.id) : edge.id}
        
        '''
        self.relationships = {
           "Institution": {
               "UMD": [...] #all nodes with “Institution” relationship, “UMD” value 
               "Yale": [...]
           },
           "Age": {
               "21": [...] #all nodes with “Age” relationship, “21” value
               "34": [...]
           }
           "Coauthor": {
               "Paper Name": [.....] #ALL AUTHOR NODES 
               "Paper Name2": [...]
           }
        }
        '''

    def return_nxGraph(self):
        return self.nxGraph

    # assumes new node is to be added
    def add_node(self, name: str, attributes: dict):
        node = Node(name, attributes)
        self.nodes[node.getID()] = node
        print("Creating new node:", node.getName())
        print("Node id:", node.getID())
        print("Node attributes:", node.getAttributes())
        return node

    # adds a new edge
    def add_edge(self, node1: Node, node2: Node, attributes: dict):
        edge = Edge(node1, node2, attributes)
        self.edges[edge.getID()] = edge
        self.connections[(node1.getID(), node2.getID())] = edge.getID()
        return edge
        
    # updates a existing node
    def update_node(self, node: Node, attributes: dict):
        print("Updating node:", node.getName())
        print("Node id:", node.getID())
        print("Node attributes:", node.getAttributes())
        node.updateAttributes(attributes)
        return node

    # might change later; so keeping it here for now
    def update_edge(self, edge: Edge, attributes: dict):
        edge.updateRelationships(attributes)
        return edge

    # returns a list of nodes that have the inputted name
    def search_named_nodes(self, name: str):
        named_nodes = []
        for node_id,node in self.nodes.items():
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
            # If two nodes are provided, search for edges between those nodes
            for (n1_id, n2_id), edge_id in self.connections.items():
                if (n1_id == node1.getID() and n2_id == node2.getID()) or (n1_id == node2.getID() and n2_id == node1.getID()):
                    edge_objects.append(self.edges[edge_id])

        return edge_objects

    # first attempt for solving disambiguity
    # named_nodes is the list of nodes with the inputted name
    # returns the node object created/updated
    # probably should be moved to functions.py
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
        print("Enter the number of the node you want or 0 to create a new one: ")
        choice = 0
        '''while True:
            choice = input(f"Enter the number of the node you want or 0 to create a new one: ")
            if choice.isdigit() and 0 <= int(choice) <= last_number:
                choice = int(choice)
                break
            print("Invalid input. Please enter a valid number.")'''

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

    def get_node(self, node_id: int):
        if node_id in self.nodes:
            return self.nodes[node_id]
        else:
            return None
        
    def print_nodes(self):
        for node in self.nodes.values():
            print()
            print(node.getName())
            print(node.getID())
            print(node.getAttributes())
