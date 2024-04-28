from GraphClass import Graph
from NodeClass import Node
from EdgeClass import Edge
from AuthorNode import AuthorNode
from parse import parseData
import networkx as nx
from SemanticScholarFuncs import *
import copy
from pyvis.network import Network
import pandas
import dask.dataframe as dd
from keys import *

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

                directed_dict = []

                if DIRECTED in attribute:
                    # stores the tuple of relationship values (like Mentor,Mentee)
                    directed_dict = attribute.pop(DIRECTED)

                node1 = create_graph_helper(graph, name1, attribute)
                node2 = create_graph_helper(graph, name2, attribute)

                # popping out directed will cause an issue if there is at least one new node (from the csv file) that only has a directed relationship with another node
                # this is because each node will have an empty attribute and therefore have no common attributes -> no common attributes means no edge will be created
                # as such we will need to create an edge between two said nodes

                if directed_dict:  # and (node1 != node2):
                    edge_list = graph.search_edge(node1, node2)

                    if not edge_list:
                        edge = graph.add_edge(node1, node2, {})

                    else:
                        edge = edge_list[0]

                    for tuple_rel in directed_dict:
                        # update node1.directed
                        node1.addDirected(node2, tuple_rel[1])

                        # update node2.directed
                        node2.addDirected(node1, tuple_rel[0])

                        # need to consider the case when the edge has already been created and the nodes were switched
                        if edge.node1 == node1:
                            edge.addDirected(tuple_rel)
                            graph.add_directed(node1, node2, tuple_rel)

                        else:
                            tuple_list_rev = (tuple_rel[1], tuple_rel[0])
                            edge.addDirected(tuple_list_rev)
                            graph.add_directed(node2, node1, tuple_list_rev)
    graph.generateColors()
    return graph


def SemanticSearch(author_name: str, choice: int = 1, numpapers: int = 5):
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
    (coauthors_dict, coauthor_mapping) = generate_author_dict(
        author_name, choice, numpapers
    )
    coauthor_list = list(coauthor_mapping.values())
    # papers_list = list(coauthors_dict.keys())

    ssgraph = CreateGraph()

    for author in coauthor_list:
        author.attributes = {}
        author.attributes[COAUTHOR] = author.papers
        ssgraph.nodes[author.id] = author

        link_nodes(ssgraph, author, author.getAttributes())

    # creates redunant AuthorNodes but for now (CDR) this will do
    # AddNodes(ssgraph,coauthor_list)
    ssgraph.generateColors()
    return ssgraph


# add nodes to a previously defined graph
# takes in a graph object and a list of nodes to be added to that graph object
# will automatically creates a new node even if a node with the same name already exists -> will not update any exisiting node in the graph
# otherwise the user can use MergeGraph
def AddNodes(graph: Graph, nodes_list: list[Node]):
    new_node_list = (
        []
    )  # if node from one graph is added to another graph, keeps the data objects separate
    new_node = None
    update_directed = []

    for node in nodes_list:
        if isinstance(node, AuthorNode):
            name = node.name
            attribute = node.attributes
            aliases = node.aliases
            authorId = node.authorId
            url = node.url
            papers = node.papers
            new_node = graph.add_ssnode(name, attribute, aliases, authorId, url, papers)
            link_nodes(graph, new_node, attribute)

        else:
            name = node.name
            attribute = node.attributes
            new_node = graph.add_node(name, attribute)
            link_nodes(graph, new_node, attribute)

        new_node_list.append(new_node)

    # for handling directed nodes
    for node, new_node in zip(nodes_list, new_node_list):
        update_directed.append(node)

        for other_node in node.directed:

            # for efficiency purposes
            if other_node not in update_directed and other_node in nodes_list:

                new_tuple_list = None
                index = nodes_list.index(other_node)
                new_other_node = new_node_list[index]

                rel = copy.deepcopy(node.directed[other_node])
                other_rel = copy.deepcopy(other_node.directed[node])

                for single_rel in rel:
                    new_node.addDirected(new_other_node, single_rel)

                for single_rel in other_rel:
                    new_other_node.addDirected(new_node, single_rel)

                new_edge = graph.search_edge(new_node, new_other_node)

                if not new_edge:
                    new_edge = graph.add_edge(new_node, new_other_node, {})

                else:
                    new_edge = new_edge[0]

                if new_edge.node1 == new_node:
                    for single_rel in zip(rel, other_rel):
                        graph.add_directed(new_node, new_other_node, single_rel)
                        new_edge.addDirected(single_rel)

                else:
                    for single_rel in zip(other_rel, rel):
                        graph.add_directed(new_other_node, new_node, single_rel)
                        new_edge.addDirected(single_rel)

    graph.generateColors()
    return graph


# creates a new graph centered around chosen_node and other nodes connected to it from the inputted graph
def SubGraph(graph: Graph, chosen_node: Node):

    if not isinstance(chosen_node, Node):
        raise ValueError("Non-Node object passed as base of subgraph.")

    # is the chosen node even in the graph?
    if chosen_node.getID() not in graph.get_nodes_dict():
        raise ValueError("Node is not in the graph")

    subgraph = CreateGraph()

    # returns all edges connected to the chosen node
    connected_edges = graph.search_edge(chosen_node)
    # used to store all nodes in the new graph
    connected_nodes = [chosen_node]
    # iterates to find other nodes in the edge
    for edge in connected_edges:

        node1 = edge.node1
        node2 = edge.node2

        # second node is the chosen node; first node is the other connected node in that edge
        if node1.id != chosen_node.id:
            connected_nodes.append(node1)
        else:
            connected_nodes.append(node2)

    # adding connected nodes to subgraph
    AddNodes(subgraph, connected_nodes)
    return subgraph


# returns a Graph of nodes that have the passed attributes
# if anything is empty/None, it will return everything
# attributes should be a dict like {str:[str]}
def FilterGraph(graph: Graph, attributes: dict = None, lamb=None):

    filter_graph = CreateGraph()
    future_nodes = []

    # lambda's will take a node and return True or False. If False, node will be filtered out
    if lamb:

        for node_id, node in graph.nodes.items():
            if lamb(node):
                future_nodes.append(node)

    else:
        if not dict:
            raise ValueError("Desired filter is not in dictionary wrapper")

        attributes = format_dict(attributes)

        # get all nodes with relationships and relationship values desired in attributes parameter
        for attr, attr_list in attributes.items():  # "age": "21"

            attr = attr.title()

            if attr in graph.relationships and attr != COAUTHOR:

                for value, value_list in graph.relationships[attr].items():

                    value = value.title()
                    if (attr_list and value in attr_list) or not attr_list:
                        for node in value_list:
                            if node not in future_nodes:
                                future_nodes.append(node)
            else:
                # if COAUTHOR was passed, means paper list is the corresponding value_list
                for value, value_list in graph.relationships[attr].items():
                    # COAUTHOR: [author1, author2]
                    for author in value_list:
                        # author1
                        for paper in attr_list:
                            # paper1
                            if paper in author.papers and author not in future_nodes:
                                future_nodes.append(author)

        """
        # get rid of unwanted filter attributes
        for node in future_nodes:
            new_attr = {}

            # go through current node's attributes' keys and values
            for attr, values in node.attributes.items():
                # if relationship in desired filter
                attr = attr.title()
                if attr in attributes:
                    # if desired filter has desired values get values that exist
                    if attributes[attr] != [] and attributes[attr] != None:
                        new_values = []
                        for v in values:
                            if isinstance(v, str):
                                v = v.title()
                            # this means that the passed in filter dictionary has to be following .title() format
                            if v in attributes[attr]:
                                new_values.append(v)

                        # if there was a desired value in the nodes existing values
                        if new_values != []:
                            new_attr[attr] = values
                    # no specified desired values, take all values
                    else:
                        new_attr[attr] = values

            node.attributes = new_attr
        """

    AddNodes(filter_graph, future_nodes)
    return filter_graph


# helper function for FilterGraph
def format_dict(attributes: dict):
    formatted = {}

    for attribute_type, attribute_values in attributes.items():

        attribute_type = attribute_type.title()
        formatted[attribute_type] = []

        if attribute_values and attribute_type != COAUTHOR:
            for attribute_value in attribute_values:
                if not isinstance(attribute_value, str):
                    attribute_value = str(attribute_value)

                formatted[attribute_type].append(attribute_value.title())
        else:
            formatted[attribute_type] = attribute_values

    return formatted


# returns a dict
# key is the name
# value is a list of nodes with that name
def Collision(graph1: Graph, graph2: Graph, list_return=False):
    nodes1 = graph1.get_nodes()
    nodes2 = graph2.get_nodes()
    collision_dict = {}

    for node in nodes1:
        if isinstance(node, AuthorNode):
            names = [node.name] + node.aliases
            for name in names:
                if name in collision_dict:
                    collision_dict[name].append(node)
                else:
                    collision_dict[name] = [node]
        else:
            node_name = node.getName()
            if node_name in collision_dict:
                collision_dict[node_name].append(node)

            else:
                collision_dict[node_name] = [node]

    for node in nodes2:
        if isinstance(node, AuthorNode):
            names = [node.name] + node.aliases
            for name in names:
                if name in collision_dict:
                    collision_dict[name].append(node)
                else:
                    collision_dict[name] = [node]
        else:
            node_name = node.getName()
            if node_name in collision_dict:
                collision_dict[node_name].append(node)

            else:
                collision_dict[node_name] = [node]

    final_dict = {}

    # if an AuthorNode from Semantic Scholar, hypothetically even if they have the same name, they all have the same aliases
    # therefore, the above code would put all nodes with different names but the same aliases in every alias-key pairing.

    for key, value in collision_dict.items():
        if len(value) > 1:
            check_node = value[0]
            if isinstance(check_node, AuthorNode):
                replace_k = ""
                for k_copy, v_copy in final_dict.items():
                    if check_node in v_copy:
                        # AuthorNodes with this alias have already been added to final_dict
                        if len(k_copy) < len(key):
                            # take longest name descriptor from aliases
                            replace_k = k_copy
                            break
                        else:
                            # this list of nodes with same names/aliases has already been added to final_dict
                            replace_k = "ALREADY EXISTS"
                            break

                if len(replace_k) != 0:
                    "THIS IS WHERE DELETING HAPPENS"
                    if replace_k != "ALREADY EXISTS":
                        del final_dict[replace_k]
                        final_dict[key] = value
                else:
                    final_dict[key] = value

            else:
                # don't need to worry about aliases
                final_dict[key] = value

    # Reset name of nodes when merge occurs with this collision list
    for k, v in final_dict.items():
        for node in v:
            node.name = k

    if not list_return:
        return final_dict
    else:
        return CollisionList(final_dict)


def CollisionList(col_dict):
    col = []

    for name, pair in col_dict.items():
        col.append(pair)

    return col


"""def clean_graphs(graph1: Graph, graph2: Graph, merge_list: list):
    for tuple in merge_list:
        for node in tuple:
            if node.id in graph1.nodes:
                del graph1.nodes[node.id]
            else:
                del graph2.nodes[node.id]

    return graph1, graph2
"""


def takecare_directed(merged_node: Node, old_nodes: dict):
    directed = merged_node.directed

    for buddy, list in directed.items():
        for old_node in old_nodes:
            if old_node in buddy.directed:
                old_props = buddy.directed[old_node]
                del buddy.directed[old_node]
                buddy.directed[merged_node] = old_props


def MergeGraph(graph1: Graph, graph2: Graph, merge_list: list = None):

    merge_graph = CreateGraph()

    # no merging
    if merge_list == None or merge_list == []:
        AddNodes(merge_graph, list(graph1.nodes.values()))
        AddNodes(merge_graph, list(graph2.nodes.values()))

    # currently assuming that nodes in merge_list are present in the graphs
    # also currently assuming that the tuples only have nodes with the same name -> prob need a helper function to check
    # also currently assuming that the same node cannot be in multiple diff tuples
    # assumes that nodes in the tuples are in the graph
    else:

        # remove nodes being merge from existing graphs
        # graph1, graph2 = clean_graphs(graph1, graph2, merge_list)

        # stores list of nodes that were merged; used to make sure we dont over merge shit
        merge = []
        # stores new nodes to be added
        nodes_list = []

        for merge_nodes in merge_list:

            # merged_nodes = [paul1, paul2, paul3]

            new_directed_set = []
            # iterating through tuple
            name = None
            attribute = {}
            # checks to see if an authornode was merged
            counter = 0

            aliases = []
            authorId = None
            url = ""
            papers = []

            # for merged nodes
            for node in merge_nodes:
                # for directed people in paul1.directed
                for bud, descrip in node.directed.items():
                    if (bud, descrip) not in new_directed_set:
                        new_directed_set.append((bud, descrip))

                name = node.name
                merge.append(node.getID())

                # Update attribute dictionary
                for key, value in node.attributes.items():
                    # iterate through each value in relationship values
                    for v in value:
                        if key in attribute and v not in attribute[key]:
                            attribute[key].append(v)
                        # Extend the existing list
                        else:
                            attribute[key] = value
                            break

                    # Add a new key-value pair if it doesn't exist

                if isinstance(node, AuthorNode):
                    # needs to be addressed
                    aliases = list(set(aliases + node.aliases))
                    authorId = node.authorId
                    url = node.url
                    papers = list(set(papers + node.papers))
                    counter = 1

            if counter == 1:
                merged_node = AuthorNode(
                    name, attribute, aliases, authorId, url, papers
                )
            else:
                merged_node = Node(name, attribute)

            # update self.nodes
            nodes_list.append(merged_node)

            if len(new_directed_set) > 0:
                # make a new directed dictionary for new node from all merged nodes
                direc_dict = {}
                # put person and associated list in new directed dictionary
                for person, l in new_directed_set:
                    # if person already in new directed dictionary
                    if person in direc_dict:
                        for prop in l:
                            # if new type of directed relationship, add
                            if prop not in direc_dict[person]:
                                direc_dict[person].append(prop)
                    else:
                        direc_dict[person] = l

                merged_node.directed = direc_dict
                # new_paul.directed = [paul1, paul2, paul3]
                takecare_directed(merged_node, merge_nodes)

        all_nodes = list(graph1.nodes.values()) + list(graph2.nodes.values())
        # for unmerged nodes
        for node in all_nodes:
            if node.getID() not in merge:
                nodes_list.append(node)

        AddNodes(merge_graph, nodes_list)

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
    node = None
    # if empty -> no node with the name was found
    if not named_nodes:
        node = graph.add_node(name, attribute)

    # if node with the inputted name was found, it returns a list with one element for which we'll need to update attributes
    else:
        node = graph.update_node(named_nodes[0], attribute)

    link_nodes(graph, node, attribute)

    return node


# essentially updates relationships dict and edge information
def link_nodes(graph: Graph, node: Node, attribute: dict):
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

                for relationship_node in relationship_nodes:
                    # checks to see if theres an exisitng edge between the two nodes
                    # makes sure it doesnt create an edge with itself
                    if relationship_node != node:
                        relationship_node = graph.get_node(relationship_node.getID())
                        edge = graph.search_edge(node, relationship_node)

                        # if there was no edge
                        if not edge:
                            graph.add_edge(node, relationship_node, temp_dict)

                        # else update the edge
                        else:
                            graph.update_edge(edge[0], temp_dict)


def NodeFromGraph(graph: Graph, name: str):
    name = name.title()
    node_list = []

    for node_id, node in graph.nodes.items():
        if node.name == name:
            node_list.append(node)

    return node_list[0] if len(node_list) == 1 else node_list


def NamesInGraph(graph: Graph):
    name_set = set()

    for node_id, node in graph.nodes.items():
        name_set.add(node.name)

    return sorted(list(name_set))


def ShortestPath(source: Node, target: Node, graph: Graph) -> list:
    # if 'graph' is 'None', returns a list of node id's, otherwise returns a list of nodes
    net = Networkx(graph)
    sp = nx.shortest_path(net, source=source.id, target=target.id)

    node_sp = []

    for id in sp:
        if id in graph.nodes:
            node_sp.append(graph.nodes[id])
        else:
            raise ValueError("Networkx object and Graph object are not equivalent")

    return node_sp


# this takes the Graph Object with the associated ntx object, and just wraps it in pyvis
def Vis(graph: Graph):

    ntx = Networkx(graph)
    pos = nx.kamada_kawai_layout(ntx, scale=1000)

    nt = Network("500px", "500px", select_menu=True)

    for node_id in ntx.nodes():
        if isinstance(graph.nodes[node_id], AuthorNode):
            nt.add_node(
                node_id,
                label=ntx.nodes[node_id]["label"],
                title=ntx.nodes[node_id]["title"],
                x=pos[node_id][0],
                y=pos[node_id][1],
                physics=False,
                font="55px arial black",
            )
        elif len(graph.nodes[node_id].directed) > 0:
            nt.add_node(
                node_id,
                label=ntx.nodes[node_id]["label"],
                title=ntx.nodes[node_id]["title"],
                x=pos[node_id][0],
                y=pos[node_id][1],
                physics=False,
                font="55px arial red",
            )
        else:
            nt.add_node(
                node_id,
                label=ntx.nodes[node_id]["label"],
                title=ntx.nodes[node_id]["title"],
                x=pos[node_id][0],
                y=pos[node_id][1],
                physics=False,
                font="55px arial blue",
            )

    for u, v, data in ntx.edges(data=True):
        nt.add_edge(
            u, v, title=data["title"], color="rgb{}".format(data["color"]), width=3.6
        )

    nt.show(
        "ntx.html", notebook=False
    )  # something between frontend/backend happens here for rendering, but this is the basics


# maybe add a function that shows first/second level connections between nodes


def Networkx(graph):
    # potentially show who person is connected to as well
    ntx = nx.Graph()

    # add nodes to networkx object
    for node_id, node in graph.nodes.items():

        title = titelize_node(node)

        if isinstance(node, AuthorNode):
            if len(node.aliases) != 0:
                aliases = "Alisases: " + ", ".join(node.aliases) + "\n"
            else:
                aliases = ""
            papers = paper_string(node.papers)
            title = (
                "Name: "
                + node.name
                + "\nID: "
                + str(node_id)
                + "\n"
                + aliases
                + papers
                + title
            )

        ntx.add_node(node_id, title=title, label=node.name)

    # add edges to networkx object
    for (node1_id, node2_id), edge_id in graph.connections.items():
        title = titelize_edge(graph.edges[edge_id])
        edge_relationships = list(graph.edges[edge_id].relationships.keys())

        # Ranking of graph relationships
        if graph.edges[edge_id].directed != []:
            color = DIRECTED_COLOR
        elif COAUTHOR in edge_relationships:
            color = COAUTHOR_COLOR
        else:
            color = graph.colors[edge_relationships[0]]

        ntx.add_edge(node1_id, node2_id, title=title, color=color)

    return ntx


def UpdateNodeAttributes(graph, node, attributes: dict):
    if node.id not in graph.nodes:
        raise ValueError("Node passed does not belong to graph passed.")

    node.updateAttributes(attributes)
    link_nodes(graph, node, attributes)


def NodeCentrality(graph, node):
    ntx = Networkx(graph)

    cent_dict = nx.degree_centrality(ntx)

    return cent_dict[node.id]


def titelize_node(node) -> str:
    directed_title = "--DIRECTED RELATIONSHIPS--\n"
    attribute_title = "--ATTRIBUTES--\n"

    direc_count = 0
    for person, value_list in node.directed.items():
        directed_title += person.name + ": "
        counter = 0

        for value in value_list:
            counter += 1
            if counter != len(value_list):
                directed_title += value + ", "
            else:
                directed_title += value

        if direc_count != len(node.directed):
            directed_title += "\n"

    # k should be String, v should be List
    for k, v in node.attributes.items():
        if k != COAUTHOR:
            attribute_title += k + ": " + ", ".join(v) + "\n"
        else:
            attribute_title += k.title() + "\n"

    if (
        directed_title != "--DIRECTED RELATIONSHIPS--\n"
        and attribute_title != "--ATTRIBUTES--\n"
    ):
        return directed_title + "\n\n" + attribute_title
    elif directed_title != "--DIRECTED RELATIONSHIPS--\n":
        return directed_title
    else:
        return attribute_title


def titelize_edge(edge: Edge) -> str:
    directed_title = ""
    attribute_title = ""

    if edge.directed != []:
        if len(edge.directed) == 1:
            directed_title += "--DIRECTED RELATIONSHIP--\n"
        else:
            directed_title += "--DIRECTED RELATIONSHIPS--\n"
        for front, back in edge.directed:
            directed_title += (
                front
                + ": "
                + edge.node1.name
                + " --> "
                + back
                + ": "
                + edge.node2.name
                + "\n"
            )

    # k should be String, v should be List
    for k, v in edge.relationships.items():
        attribute_title = "--SHARED ATTRIBUTES--\n"
        if k != COAUTHOR:
            attribute_title += k + ": " + ", ".join(v) + "\n"

        if COAUTHOR in edge.relationships:
            if attribute_title == "--SHARED ATTRIBUTES--\n":
                attribute_title = "--SHARED PAPERS--\n"
                for paper in v:
                    attribute_title += paper.title + "\n"
            else:
                attribute_title += "--SHARED PAPERS--\n"
                for paper in v:
                    attribute_title += paper.title + "\n"

    if len(directed_title) != 0 and len(attribute_title) != 0:
        return directed_title + "\n\n" + attribute_title
    elif len(directed_title) != 0:
        return directed_title
    else:
        return attribute_title


def paper_string(papers) -> str:
    title = "--PAPERS--\n"

    for paper in papers:
        title += paper.title + ": " + str(paper.year) + "\n"

    return title


def saveData(nodes, filePath):
    names = list()
    attributes = list()
    authors = list()

    # Gets all information out of the list of nodes, and sorts into authors and non authors
    for node in nodes:
        if type(node) is AuthorNode:
            authors.append(node)
        else:
            names.append(node.getName())
            attributes.append(node.getAttributes())

    # Formats non author data in the correct way
    data = dict()
    ks = list()
    vs = list()
    for x in attributes:

        keyslist = list(x.keys())
        valuelist = list(x.values())
        values_to_save = list()
        keys_to_save = list()

        # Unpacks list of lists into values
        for y in range(len(valuelist)):
            for z in range(len(valuelist[y])):
                keys_to_save.append(keyslist[y])
                values_to_save.append(valuelist[y][z])

        ks.append(",".join(keys_to_save))
        vs.append(",".join(values_to_save))

    for x in authors:
        keys_to_save = list()
        values_to_save = list()
        keys_to_save.append("AUTHORID")
        values_to_save.append(x.authorId)
        for i in range(len(x.papers)):
            keys_to_save.append("PAPER")
            values_to_save.append(x.papers[i].title)

        names.append(x.getName())
        ks.append(",".join(keys_to_save))
        vs.append(",".join(values_to_save))

    # Puts all data into a dictionary
    data["Person 1"] = names
    data["Relationship"] = ks
    data["Relationship Value"] = vs

    # Saves dictionary to csv
    pandas_df = pandas.DataFrame(data)
    df = dd.from_pandas(pandas_df, npartitions=1)
    df.compute().to_csv(filePath, index=False)
