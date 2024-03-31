from Graph import Graph
from Node import Node
from Edge import Edge
from parse import parseData
import copy

# for both Graph.py and Functions.py, some functions could return int's instead of node/edge/graph objects since changes are already made in the function inside
# having int return (on the based of node/edge creation) could speed up shit
# could also return tuple of (object,int)

# creates a new Graph object from scratch and add nodes to it
# could change the return type
def CreateGraph(csv):
    G = Graph()
    AddNodes(G,csv)
    # not needed
    return G

# add nodes to a previously defined graph
# could change the return type
def AddNodes(graph: Graph, csv):
    
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
                    
    return graph

def SubGraph(graph: Graph, name: str):
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
