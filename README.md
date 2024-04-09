# New Connections Use Guide

This guide will walk you through currently active functions to be used in our REPL. 

## Website

http://vegetable.cs.umd.edu:3000/

## Functions

1. MergeGraph:

    MergeGraph(graph1: Graph, graph2: Graph, merge_list: list = None)

    Description: 
    Merges two input graphs into a single graph. It allows merging specific nodes from each graph based on the provided merge_list. Merge_list is a list that contains tuples of nodes from the two graphs. Nodes in tuples are merged together in the new graph. Any node not in merge_list will not be merged with any other node. If no merge list is provided, it will not merge any nodes and all the nodes from both graphs will be added to the new graph.

    Usage Prototype/Example:

   ```
   merged_graph = MergeGraph(graph1, graph2, [(node1_graph1, node2_graph2), (node3_graph1, node4_graph2)])
   ```
   
2. CreateGraph:

    CreateGraph(csv: str = None)

    Description: 
    Creates a new graph object, populated with nodes from the CSV file uploaded on the App.
    The user is expected to upload a file (say with name "data.csv") and pass the name of the file as a string. (e.g. CreateGraph("data.csv")).
    An error will be generated if no csv file was uploaded if a string was passed.
    If no parameter is provided, an empty graph is generated. 

    Note:
	    i) Currently cannot handle Directed Relationships
	    ii) Currently does not have any Semantic Scholar implementation


    Usage Prototype/Example:

   ```
   graph = CreateGraph("data.csv")
   ```
   
3. FilterGraph:

    FilterGraph(graph: Graph, attributes: dict = None)

    Description: 
    Filters the nodes of the input graph based on specified attributes dictionary.
    Attributes should be a dictionary where the key is a string whose corresponding values is a list of strings. Returns a new graph object containing only the nodes that match the given attributes.

    Usage Prototype/Example:

   ```
   filtered_graph = FilterGraph(filtered_graph, attributes={"attribute1": ["value1"], "attribute2": [“value2”,”value3”]
   ```
   
4. Networkx:

    Description: 
    Converts the input graph object into a NetworkX graph object.
    Prepares the graph for further analysis and visualization using the NetworkX library.


    Usage Prototype/Example:

   ```
   ntx_graph = Networkx(graph)
   ```

5. Vis:

    Vis(ntx_graph)

    Description: 
    Visualizes the Networkx Object using the Pyvis library.
    Generates an interactive HTML visualization of the graph.


    Usage Prototype/Example:

   ```
   Vis(networkx_graph)
   ```

