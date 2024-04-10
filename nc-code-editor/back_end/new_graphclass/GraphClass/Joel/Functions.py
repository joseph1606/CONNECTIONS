from GraphClass import Graph
from NodeClass import Node
from EdgeClass import Edge
from AuthorNode import AuthorNode
from parse import parseData
import networkx as nx
from SemanticScholarFuncs import *

# from SemanticScholarFuncs import generate_author_dict

# if a csv was inputted, it will create nodes based off the csv
# else (in the case of no input) it will just create an empty graph -> user can use AddNodes to add nodes to it
def CreateGraph(csv: str = None):
    graph = Graph()

    # case when we need to create nodes from a csv file
    if csv:
        (names1, names2, attributes) = parseData(csv)

        if names2 is None:
            # iterates through each row of inputs from csv
            for name, attribute in zip(names1, attributes):
                create_graph_helper(graph, name, attribute)

        else:
            for name1, name2, attribute in zip(names1, names2, attributes):
                create_graph_helper(graph, name1, attribute)

                create_graph_helper(graph, name2, attribute)
    graph.generateColors()
    return graph


def SSCreateGraph(author_name:str,choice:int=1, numpapers:int=5):
    """
    coauthors_dict:
    PaperNode1: [list of AuthorNodes]
    PaperNode2: [list of AuthorNodes]
    .....
    
    coauthor_mapping:
    AuthorNode.id : AuthorNode
    
    coauthor_list = [list of AuthorNodes]
    
    papers_list = [list of Unique PaperNodes]
    """
    
    (coauthors_dict, coauthor_mapping) = generate_author_dict(author_name,choice, numpapers)
    coauthor_list = list(coauthor_mapping.values())
    papers_list = list(coauthors_dict.keys())
    
    for author in coauthor_list:
        paper_titles = []
        for paper in author.papers:
            # should change this to just papers
            paper_titles.append(paper)
  
        author.attributes = {}
        author.attributes["papers"] = paper_titles

    ssgraph = CreateGraph()
 
    # creates redunant AuthorNodes but for now (CDR) this will do
    AddNodes(ssgraph,coauthor_list)
    
    
    return ssgraph
    

# add nodes to a previously defined graph
# takes in a graph object and a list of nodes to be added to that graph object
# will automatically creates a new node even if a node with the same name already exists -> will not update any exisiting node in the graph
# otherwise the user can use MergeGraph
def AddNodes(graph: Graph, nodes_list: list[Node]):

    for node in nodes_list:
        if isinstance(node,AuthorNode):
            name = node.getName()
            attribute = node.getAttributes()
            aliases = node.aliases
            authorId = node.authorId
            url = node.url
            papers = node.papers
            node = graph.add_ssnode(name,attribute,aliases,authorId,url,papers)
            link_nodes(graph, node, attribute)
                   
        else:
            name = node.getName()
            attribute = node.getAttributes()
            node = graph.add_node(name, attribute)
            link_nodes(graph, node, attribute)

    return graph


# creates a new graph centered around chosen_node and other nodes connected to it from the inputted graph
def SubGraph(graph: Graph, chosen_node: Node):

    # is the chosen node even in the graph?
    if chosen_node.getID() not in graph.get_nodes_dict():
        # print("Node is not in the graph")
        raise ValueError("Node is not in the graph")

    subgraph = CreateGraph()

    # to avoid interconnected nodes
    name = chosen_node.getName()
    attribute = chosen_node.getAttributes()

    node = Node(name, attribute)

    # returns all edges connected to the chosen node
    connected_edges = graph.search_edge(chosen_node)
    # used to store all nodes in the new graph
    connected_nodes = [node]
    # iterates to find other nodes in the edge
    for edge in connected_edges:

        node1 = edge.getNode1()
        node2 = edge.getNode2()

        # second node is the chosen node; first node is the other connected node in that edge
        if node1.getID() != chosen_node.getID():
            connected_nodes.append(node1)
        else:
            connected_nodes.append(node2)

    # adding connected nodes to subgraph
    AddNodes(subgraph, connected_nodes)
    subgraph.generateColors()
    return subgraph


# returns a Graph of nodes that have the passed attributes
# if anything is empty/None, it will return everything
# attributes should be a dict like {str:[str]}
# need to convert attributes dict to proper format
def FilterGraph(graph: Graph, attributes: dict = None):

    if not dict:
        return None

    filter_graph = CreateGraph()
    attributes = format_dict(attributes)

    future_nodes = []

    for attr, attr_list in attributes.items():
        relat_dict = graph.relationships[attr]

        for value, value_list in relat_dict.items():
            if (attr_list and value in attr_list) or not attr_list:
                future_nodes += value_list

    for i in range(len(future_nodes)):
        future_nodes[i] = graph.nodes[future_nodes[i]]

    AddNodes(filter_graph, future_nodes)
    filter_graph.generateColors()
    return filter_graph


# helper function for FilterGraph
def format_dict(attributes: dict):
    formatted = {}

    for attribute_type, attribute_values in attributes.items():
        attribute_type = attribute_type.lower()
        formatted[attribute_type] = []

        for attribute_value in attribute_values:
            formatted[attribute_type].append(attribute_value.lower())

    return formatted


# returns a dict
# key is the name
# value is a list of nodes with that name
def Collision(graph1: Graph, graph2: Graph):
    nodes1 = graph1.get_nodes()
    nodes2 = graph2.get_nodes()
    collision_dict = {}

    for node in nodes1:
        node_name = node.getName()
        if node_name in collision_dict:
            collision_dict[node_name].append(node)

        else:
            collision_dict[node_name] = [node]

    for node in nodes2:
        node_name = node.getName()
        if node_name in collision_dict:
            collision_dict[node_name].append(node)

        else:
            collision_dict[node_name] = [node]

    for key, value in collision_dict.items():
        if len(value) <= 1:
            del collision_dict[key]

    return collision_dict


def MergeGraph(graph1: Graph, graph2: Graph, merge_list: list = None):
    merge_graph = CreateGraph()
    nodes1 = graph1.get_nodes()
    nodes2 = graph2.get_nodes()

    # no merging
    if merge_list == None or merge_list == []:
        AddNodes(merge_graph, nodes1)
        AddNodes(merge_graph, nodes2)

    # currently assuming that nodes in merge_list are present in the graphs
    # also currently assuming that the tuples only have nodes with the same name -> prob need a helper function to check
    # also currently assuming that the same node cannot be in multiple diff tuples
    else:
        # stores list of nodes that were merged; used to make sure we dont over merge shit
        merge = []
        # stores new nodes to be added
        nodes_list = []
        for merge_nodes in merge_list:
            # iterating through tuple
            name = None
            attribute = {}

            # for merged nodes        
            for node in merge_nodes:
                name = node.getName()
                node_attributes = node.getAttributes()
                
                # Update attribute dictionary
                for key, value in node_attributes.items():
                    if key in attribute:
                        attribute[key].extend(value)  # Extend the existing list
                    else:
                        attribute[key] = value  # Add a new key-value pair if it doesn't exist
                
                merge.append(node.getID())

            merged_node = Node(name, attribute)
            nodes_list.append(merged_node)

        all_nodes = nodes1 + nodes2
        # for unmerged nodes
        for node in all_nodes:
            if node.getID() not in merge:
                name = node.getName()
                attribute = node.getAttributes()
                nodes_list.append(node)

        AddNodes(merge_graph, nodes_list)

    merge_graph.generateColors()
    return merge_graph


# returns a list of Nodes in a Graph
def GetNodes(graph: Graph):
    return graph.get_nodes()


# helper function for filter
def common_ids(list_of_lists):
    if not list_of_lists:
        return []

    # Convert the first inner list to a set
    result_set = set(list_of_lists[0])

    # Iterate through the rest of the inner lists and find their intersection with the result set
    for lst in list_of_lists[1:]:
        result_set.intersection_update(set(lst))

    # Convert the result set back to a list
    result_list = list(result_set)

    return result_list


# helper function to create graphs -> uses link_nodes which is needed
def create_graph_helper(graph: Graph, name: str, attribute: dict):

    named_nodes = graph.search_named_nodes(name)

    # if empty -> no node with the name was found
    if not named_nodes:
        node = graph.add_node(name, attribute)

    # if node with the inputted name was found, it returns a list with one element for which we'll need to update attributes
    else:
        node = graph.update_node(named_nodes[0], attribute)

    link_nodes(graph, node, attribute)


# essentially updates relationships dict and edge information
def link_nodes(graph: Graph, node: Node, attribute: dict):
    node_id = node.getID()
    # iterates through one row of attributes
    # eg {sex:[male], college:[umd]}
    # it iterates twice in the above example
    for attribute_type, attribute_value in attribute.items():
        temp_dict = {}
        temp_dict[attribute_type] = attribute_value

        # returns list of nodes id with the same attribute type and value that isnt the inputted node
        # note -> do i need to iterate through attribute value or will it always only haev one element
        #      -> i will prob need to iterate cuz of something like college:[umd,umbc]
        for single_attribute_value in attribute_value:
            relationship_nodes = graph.relationship_nodes(
                node, attribute_type, single_attribute_value
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


def nodeFromGraph(graph: Graph, name: str):
    node_list = []

    for node_id, node in graph.nodes.items():
        if node.name == name:
            node_list.append(node)

    return node_list


def namesInGraph(graph: Graph):
    name_set = set()

    for node_id, node in graph.nodes.items():
        name_set.add(node.name)

    return list(name_set)


def ShortestPath(
    source: Node, target: Node, graph: Graph = None, net: nx = None
) -> list:
    # if 'graph' is 'None', returns a list of node id's, otherwise returns a list of nodes
    if not graph:
        nx.shortest_path(net, source=source.id, target=target.id)

    sp = nx.shortest_path(net, source=source.id, target=target.id)
    node_sp = []

    for id in sp:
        node_sp.append(graph.nodes[id])

    return sp


# this takes the Graph Object with the associated ntx object, and just wraps it in pyvis
def Vis(ntx):
    nt = Network("500px", "500px")
    # fancy rendering here

    for node_id in ntx.nodes():
        nt.add_node(
            node_id,
            label=ntx.nodes[node_id]["label"],
            title=ntx.nodes[node_id]["title"],
            size=22,
        )

    for u, v, data in ntx.edges(data=True):
        nt.add_edge(
            u, v, title=data["title"], color="rgb{}".format(data["color"]), width=3.6
        )

    # nt.from_nx(ntx)
    nt.toggle_physics(True)
    nt.show(
        "ntx.html", notebook=False
    )  # something between frontend/backend happens here for rendering, but this is the basics


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
        edge_relationships = list(graph.edges[edge_id].relationships.keys())
        color = graph.colors[edge_relationships[0]]

        ntx.add_edge(node1_id, node2_id, title=title, color=color)

    return ntx


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
