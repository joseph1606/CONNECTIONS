import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

import GraphClass.Joel.GraphClass as Graph
import GraphClass.Joel.Edge as Edge
import GraphClass.Joel.NodeClass as Node
import GraphClass.Revaant.AuthorNode as Author
from GraphClass.Revaant.AuthorNode import AuthorNode


def CreateGraph(csv) -> Graph.Graph:
    # disambiguation with csv parsing
    # search function, user can use next or prev and then once user has a number then run
    # g = CreateGraph(name, number)
    from app import displayAuthor
    G = Graph()
    if csv != 'csv':
        #run semantic shole
        #generate_author_list(csv)
        displayAuthor(csv)
        # want to be makeAuthor not display
    else:
        file_path = '/Users/andrewtimmer/repo_connection/new_connections/pythonAPI/back_end/new_graphclass/GraphClass/Tester/Joel/data.csv'
        Add(G,file_path)
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
    
    while True:
        choice = input("Enter the number of the node you want: ")
        if choice.isdigit() and 1 <= int(choice) <= len(named_nodes):
            chosen_node = named_nodes[int(choice) - 1]
            break
        print("Invalid input. Please enter a valid number.")
    
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


def Add(graph: Graph.Graph, csv) -> Graph.Graph:
    
    # needs to capitalize first letter and lowercase the rest for name
    # everything else can be lowercase?
    (names1, names2, attributes) = parseData(csv)

    if names2 is None:
        for name, attribute in zip(names1, attributes):
            named_nodes = graph.search_named_nodes(name)
            graph.disambiguation(named_nodes, name, attribute)
            
            # no need to create an edge

    else:
        for name1, name2, attribute in zip(names1, names2, attributes):
            named_nodes1 = graph.search_named_nodes(name1)
            named_nodes2 = graph.search_named_nodes(name2)
            
            # to avoid interconnected nodes if a new node was created
            # idk why but shallow copy works
            # technically if a new node was created for named_nodes1, there wouldn't need to be a need to shallow copy
            attribute_dup = copy.copy(attribute) if attribute else {}
            
            disambiguated_node1 = graph.disambiguation(named_nodes1, name1, attribute)
            disambiguated_node2 = graph.disambiguation(named_nodes2, name2, attribute_dup)
            
            # technically if a new node was created in disambiguation there wouldn't be a need to check for an edge
            # search_edge returns a list of edges; here since two nodes are inputted it returns either an empty list or a list with just one edge
            edge_objects = graph.search_edge(disambiguated_node1, disambiguated_node2)
            
            # if there was no edge
            if not edge_objects:
                graph.add_edge(disambiguated_node1, disambiguated_node2, attribute)
                    
            # if there was an edge, search_edge returns [edge]
            else:
                graph.update_edge(edge_objects[0], attribute)
    #graph.print_nodes()   
    return graph


def Filter(graph: Graph.Graph, params: str) -> Graph.Graph:
    pass


# skip shortestPath


def Merge(graph1: Graph.Graph, graph2: Graph.Graph) -> Graph.Graph:
    pass
