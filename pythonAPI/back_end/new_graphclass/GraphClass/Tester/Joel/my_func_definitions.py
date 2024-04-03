import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from parse import parseData

import Graph as Graph
import Edge as Edge
import Node as Node
import AutherNode as AuthorNode


def CreateGraph(csv, num) -> Graph.Graph:
    # disambiguation with csv parsing
    # search function, user can use next or prev and then once user has a number then run
    # g = CreateGraph(name, number)
    from app import makeAuthor
    G = Graph()
    if csv != 'csv':
        #run semantic shole
        #generate_author_list(csv)
        makeAuthor(csv, num)
        # want to be makeAuthor not display
    else:
        file_path = '/Users/andrewtimmer/repo_connection/new_connections/pythonAPI/back_end/new_graphclass/GraphClass/Tester/Joel/data.csv'
        AddNodes(G,file_path)
    # not needed
    return G


def Subgraph(graph: Graph.Graph, name: str) -> Graph.Graph:
    named_nodes = graph.search_named_nodes(name)
    chosen_node = None
    
    if not named_nodes:
        raise ValueError("There is no such node with that name present in the graph")
    
    subgraph = Graph() 
    
    print("Nodes with name", name, "found in the graph:")
    for i, node in enumerate(named_nodes, start=1):
        print(i, ". Name:", node.getName())
        print("   Attributes:", node.getAttributes())
    
    # THIS will not work
    '''while True:
        choice = input("Enter the number of the node you want: ")
        if choice.isdigit() and 1 <= int(choice) <= len(named_nodes):
            chosen_node = named_nodes[int(choice) - 1]
            break
        print("Invalid input. Please enter a valid number.")'''
    
    subgraph.add_node(chosen_node.getName(), chosen_node.getAttributes())
    
    # returns all edges connected to the chosen node
    connected_edges = graph.search_edge(chosen_node)
    
    for edge in connected_edges:
        # if the second node is the other node; first node is the chosen node
        if edge.getNode1().getID() != chosen_node.getID():
            connected_node = edge.getNode1()
        else:
            connected_node = edge.getNode2()
            
        subgraph.add_node(connected_node.getName(), connected_node.getAttributes())
    
    return subgraph


# INTRODUCING A NEW FUNCTION (DONT DO THIS)
def Networkx(graph: Graph.Graph) -> nx.Graph:
    pass

# (DONT DO THIS)
def Vis(ntx: nx.Graph) -> Network:
    pass


def Save(graph: Graph.Graph) -> "csv":
    pass

def AddNodes(graph: Graph, csv):
    
    # needs to capitalize first letter and lowercase the rest for name
    # everything else can be lowercase?
    # names1: list[str]
    # names2: list[str]
    # attributes: list[dict]
    # eg []
    (names1, names2, attributes) = parseData(csv)

    if names2 is None:
        # iterates through each row of inputs
        for name, attribute in zip(names1, attributes):
            node = None
            named_nodes = graph.search_named_nodes(name)
            
            # if empty -> no node with the name was found
            # there will also be no edges associated with that node
            if not named_nodes:
                node = graph.add_node(name,attribute)
            
            # if node with the inputted name was found, it returns a list with one element for which we'll need to update attributes
            else:
                node = graph.update_node(named_nodes[0],attribute)

            AddNodeHelper(graph,node,attribute)
     
                
            

    else:
        for name1, name2, attribute in zip(names1, names2, attributes):
            node1 = None
            node2 = None
            named_nodes1 = graph.search_named_nodes(name1)
            named_nodes2 = graph.search_named_nodes(name2)
            
            if not named_nodes1:
                node1 = graph.add_node(name1,attribute)
            
            # if node with the inputted name was found, it returns a list with one element for which we'll need to update attributes
            else:
                node1 = graph.update_node(named_nodes1[0],attribute)
                
                
            AddNodeHelper(graph,node1,attribute)
            
            # to avoid interconnected nodes
            attribute_dup = copy.copy(attribute)
            
            if not named_nodes2:
                node2 = graph.add_node(name2,attribute_dup)
            
            # if node with the inputted name was found, it returns a list with one element for which we'll need to update attributes
            else:
                node2 = graph.update_node(named_nodes2[0],attribute_dup)
                
                
            AddNodeHelper(graph,node2,attribute)
                
                
 
    return graph

# essentially takes cares of relationships dict and edges
def AddNodeHelper(graph: Graph, node: Node, attribute: dict):
    node_id = node.getID()
    # iterates through one row of attributes
    # eg {sex:[male], college:[umd]}
    # it iterates twice in the above example
    for attribute_type, attribute_value in attribute.items():
        temp_dict = {}
        temp_dict[attribute_type] = attribute_value
        # returns list of nodes id with the same attribute type and value that isnt the inputted node
        relationship_nodes = graph.relationship_nodes(node,attribute_type,attribute_value[0])
        
        # if empty then there are currently no other nodes with that attribute type and value -> no need to create edges
        # if not empty then we need to create edges
        if relationship_nodes:
            
            for relationship_node_id in relationship_nodes:
                # checks to see if theres an exisitng edge between the two nodes
                # makes sure it doesnt create an edge with itself
                if relationship_node_id != node_id:
                    relationship_node = graph.get_node(relationship_node_id)
                    edge = graph.search_edge(node, relationship_node)
                    
                    # if there was no edge
                    if not edge:
                        graph.add_edge(node,relationship_node,temp_dict)
                        
                    # else update the edge
                    else:
                        graph.update_edge(edge[0], temp_dict)



def Filter(graph: Graph.Graph, params: str) -> Graph.Graph:
    pass


# skip shortestPath


def Merge(graph1: Graph.Graph, graph2: Graph.Graph) -> Graph.Graph:
    pass
