from GraphClass import Graph
from NodeClass import Node
from EdgeClass import Edge
from AuthorNode import AuthorNode
from parse import parseData
import copy
import networkx as nx
from pyvis.network import Network


# for both Graph.py and Functions.py, some functions could return int's instead of node/edge/graph objects since changes are already made in the function inside
# having int return (on the based of node/edge creation) could speed up shit
# could also return tuple of (object,int)


# creates a new Graph object from scratch and add nodes to it
# could change the return type
def CreateGraph(csv):
    G = Graph()
    AddNodes(G, csv)
    # not needed
    return G


# add nodes to a previously defined graph
# could change the return type
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
                node = graph.add_node(name, attribute)

            # if node with the inputted name was found, it returns a list with one element for which we'll need to update attributes
            else:
                node = graph.update_node(named_nodes[0], attribute)

            AddNodeHelper(graph, node, attribute)

    else:
        for name1, name2, attribute in zip(names1, names2, attributes):
            node1 = None
            node2 = None
            named_nodes1 = graph.search_named_nodes(name1)
            named_nodes2 = graph.search_named_nodes(name2)

            if not named_nodes1:
                node1 = graph.add_node(name1, attribute)

            # if node with the inputted name was found, it returns a list with one element for which we'll need to update attributes
            else:
                node1 = graph.update_node(named_nodes1[0], attribute)

            AddNodeHelper(graph, node1, attribute)

            # to avoid interconnected nodes
            attribute_dup = copy.copy(attribute)

            if not named_nodes2:
                node2 = graph.add_node(name2, attribute_dup)

            # if node with the inputted name was found, it returns a list with one element for which we'll need to update attributes
            else:
                node2 = graph.update_node(named_nodes2[0], attribute_dup)

            AddNodeHelper(graph, node2, attribute)

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
        relationship_nodes = graph.relationship_nodes(
            node, attribute_type, attribute_value[0]
        )

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
                        graph.add_edge(node, relationship_node, temp_dict)

                    # else update the edge
                    else:
                        graph.update_edge(edge[0], temp_dict)


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

    # could also make a deep copy instead of running it through existing functions?
    # might have to pass a shallow copy of attributes; need to check
    subgraph.add_node(chosen_node.getName(), chosen_node.getAttributes())

    # returns all edges connected to the chosen node
    connected_edges = graph.search_edge(chosen_node)

    for edge in connected_edges:
        # if the second node is the other node; first node is the chosen node
        if edge.getNode1().getID() != chosen_node.getID():
            connected_node = edge.getNode1()
        else:
            connected_node = edge.getNode2()

        # could also make a deep copy instead of running it through existing functions?
        # might have to pass a shallow copy of attributes; need to check
        subgraph.add_node(connected_node.getName(), connected_node.getAttributes())

    return subgraph

    """
    Old code that handled disambiguation
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
    """


# this takes the Graph Object with the associated ntx object, and just wraps it in pyvis
def Vis(ntx):
    nt = Network("500px", "500px")
    # fancy rendering here
    nt.from_nx(ntx)
    nt.toggle_physics(True)
    nt.show("ntx.html", notebook=False)


def Networkx(graph):
    ntx = nx.Graph()

    # add nodes to networkx object
    for node_id, node in graph.nodes.items():

        title = titelize(node.attributes)

        if type(node) is AuthorNode:
            aliases = "Alisases: " + ", ".join(node.aliases) + "\n"
            papers = paper_string(node.papers)
            title = aliases + papers + title

        ntx.add_node(node_id, title=title, label=node.name)

    # add edges to networkx object
    for (node1_id, node2_id), edge_id in graph.connections.items():
        title = titelize(graph.edges[edge_id].relationships)
        ntx.add_edge(node1_id, node2_id, title=title)

    return ntx


def ShortestPath(graph: Graph, optional, net: nx, source: Node, target: Node) -> list:
    # if 'graph' is 'None', returns a list of node id's, otherwise returns a list of nodes
    if not graph:
        nx.shortest_path(net, source=source.id, target=target.id)

    sp = nx.shortest_path(net, source=source.id, target=target.id)
    node_sp = []

    for id in sp:
        node_sp.append(graph.nodes[id])

    return sp


# NEEDS TO TAKE CARE OF DIRECTED RELATIONSHIPS
def titelize(attributes: dict) -> str:
    title = ""

    # k should be String, v should be List
    for k, v in attributes.items():
        title += k + ": " + ", ".join(v) + "\n"

    return title


def paper_string(papers) -> str:
    title = ""

    for paper in papers:
        title += paper.title + ": " + paper.year + "\n"

    return title
