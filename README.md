# New Connections Use Guide

This guide will walk you through currently active functions to be used in our REPL. 

## Website

http://vegetable.cs.umd.edu:3000/

## Setting Up Environment

### Prerequisites
npm, python3, and pip (or pip3) installed on your local machine.

### Step 1
Clone the repository to your local machine and open a terminal starting at the repository root (new_connections). From there, cd into nc-code-editor.
```console
$ cd nc-code-editor
```
Then run the frontend app:
```console
$ npm start
```

### Step 2
Open another terminal starting at the repository root (new_connections) and cd into the pythonAPI directory.
```console
$ cd pythonAPI
```
Create a virtual environment:
```console
$ python3 -m venv venv
```
Activate the environment (note the period at the begining):
```console
$ . venv/bin/activate
```
You should notice a difference in your prompt. Then install required packages with pip (or pip3):
```console
$ pip install -r requirements.txt
```
Then run the backend app:
```console
$ python3 app.py
```

## Functions
### AddNodes
#### (graph: Graph, nodes_list: List[Node]) -> Graph: 
This function adds nodes to an existing graph object. It takes a graph object (Graph) representing the target graph and a list of nodes_list (list[Node]) representing the nodes to be added to the target graph.

### Collision
#### (graph1: Graph, graph2: Graph, list_return: bool = False) -> Optional[List[List[Node]], Dict[str, List[Node]]]: 
This function identifies nodes in two graphs that have the same name. It takes two graph objects (graph1 and graph2) and an optional list_return (boolean) parameter indicating whether to return a list of collisions or a dictionary of collisions.

### CollisionList
#### (collisions: Dict[str, List[Node]]) -> Optional[List[Tuple[Node]]]: 
This function returns a list of collision pairs identified by the Collision() function. It takes a dictionary of names paired with a list of nodes with that name.

### CreateGraph
#### (csv: str = None) -> Graph: 
This function creates a new graph object, optionally populated with nodes and edges from a CSV file. It takes an optional parameter csv (string) representing the path to the CSV file containing node data. If no parameter was passed, an empty graph will be created.

### FilterGraph
#### (graph: Graph, attributes: Dict[str, List[str]] = None, lamb = None) -> Graph: 
This function filters nodes based on attributes or custom logic. It takes a graph object (graph), an optional dictionary of attributes (attributes), and an optional function (lamb). If attributes are given, it returns a new graph with nodes matching those attributes. If the optional function is provided, it filters nodes based on custom logic. 

### GetNodes
#### (graph: Graph) -> List[Node]: 
This function retrieves a list of nodes from a graph. It takes a graph object (Graph) as input.

### MergeGraph
#### (graph1: Graph, graph2: Graph, merge_list: List[Tuple[Node, Node]]) -> Graph: 
This function merges nodes from two graphs based on a specified merge list. It takes two graph objects (graph1 and graph2) and an optional merge_list (list) parameter specifying the nodes to be merged and returns the merged graph.

### NamesInGraph
#### (graph: Graph) -> List[str]: 
This function returns a sorted list of unique node names present in a graph. It takes a graph object (Graph) as input.

### NodeCentrality
#### (graph: Graph, node: Node) -> float:
This function calculates the centrality of a node in a graph. It takes two parameters: a graph object (Graph) and a node (Node) whose centrality is to be calculated.

### NodeFromGraph
#### (graph: Graph, name: str) -> Optional[Node, List[Node]]: 
This function retrieves a node from a graph based on its name. It takes a graph object (Graph) and a name (str) representing the name of the node. If only one node in the graph has that name, it returns that node. Otherwise, it returns a list of nodes with that name.

### SaveData
#### (nodes: List[Node], filePath: str) -> None:
This function saves node and relationship data from a list of nodes to a CSV file. It takes two parameters: a list of nodes and a filePath (str) representing the path to save the CSV file.

### SemanticGraph
#### (author_name: str, choice: int = 1, numpapers: int = 5) -> Graph: 
This function generates a graph representing the collaboration network of an author based on Semantic Scholar data. It takes an author's name as a string (author_name), an optional integer choice that determines the particular author to select (default is 1), and an optional integer numpapers representing the number of papers to consider (default is 5).

### ShortestPath
#### (source: Node, target: Node, graph: Graph) -> List[Node]:
This function calculates the shortest path between two nodes in a graph. It takes three parameters: a source node (Node), a target node (Node), and a graph object (Graph) and returns a list of the path of the nodes.

### SubGraph
#### (graph: Graph, chosen_node: Node) -> Graph: 
This function creates a subgraph from an existing graph centered around a chosen node. It takes a graph object (Graph) representing the original graph and a chosen_node (Node) representing the center node of the subgraph.

### UpdateNodeAttributes
#### (graph: Graph, node: Node, attributes: Dict[str, List[str]]) -> None: 
This function updates the attributes of a node in a graph. It takes three parameters: a graph object (Graph), a node (Node) belonging to the passed graph object whose attributes are to be updated, and an attributes (dict) parameter representing the new attributes.

### Vis
#### (graph: Graph) -> None:
This function generates a visualization of a graph using the Pyvis library. It takes a graph object (Graph) as input.

