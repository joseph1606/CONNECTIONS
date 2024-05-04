import "./Header.css";
import i from "./media/information-button.png"
import logo from "./media/download.png"

function popup() {
  document.getElementById('functions').style.visibility = 'visible'
  document.getElementById('functions').style.display = ''

};
function cheerdown() {
  document.getElementById('functions').style.visibility = 'hidden'
  document.getElementById('functions').style.display = 'none'
  document.getElementById('funcname').textContent = '';
  document.getElementById('desciption').textContent = '';
  document.getElementById('parameterslistedout').textContent = '';
  document.getElementById('parametertitle').textContent = '';
  document.getElementById('desctitle').textContent = '';
};

function funcpopup() {
  document.getElementById('funclist').style.height = 'fit-content';
  document.getElementById('funclist').style.visibility = 'visible'
  document.getElementById('select').style.backgroundColor = 'orange'

};
function funccheerdown() {
  document.getElementById('funclist').style.visibility = 'hidden'
  document.getElementById('select').style.backgroundColor = 'white'
};


function Header() {
  return <div>
    <div id='mainheader'>
      <div style={{ display: 'flex', backgroundColor: "white", margin: '5px', border: '2px solid grey', borderRadius: '15px', fontFamily: 'bold', marginLeft: '.5vw', minWidth: '200px', alignItems: 'center', minHeight: '5vh' }}>
        <img src={logo} alt="logo" style={{ padding: '5px', height: '6vh' }} />
        <h1 id='title' style={{ color: 'black', width: '9.5vw', height: '2.5vh', fontSize: '2.5vh' }}>Connections</h1>
      </div>
      <div id="info" style={{ border: '0px', position: 'absolute', zIndex: 3, width: '25vw', maxWidth: '25vw', right: 0 }}>
        <img id='i' src={i} alt="Info" onMouseOver={popup} onMouseLeave={cheerdown} />
        <div id="functions" style={{ visibility: 'hidden', display: 'none' }} onMouseOver={popup} onMouseLeave={cheerdown}>
          <h1>Functions</h1>
          <br />
          <div style={{ height: 'fit-content' }} onMouseLeave={funccheerdown}>
            <h4 onMouseOver={funcpopup} id='select' style={{ outline: '2px solid grey', marginLeft: '10%', marginRight: '10%', backgroundColor: 'white' }}>Select Function:</h4>
            <div id="funclist" onMouseOver={funcpopup} style={{ visibility: 'hidden', backgroundColor: 'whitesmoke', border: '1px solid grey', padding: '2px', height: '150%', position: 'absolute', width: '98%', left: '1%' }}>
              <div className="funclistitem">
                {functionDescriptions.map((funcdesc, index) => (
                  <h5 onClick={() => fillinfo(funcdesc)}>{funcdesc[0]}</h5>
                ))}

              </div>
            </div>
          </div>
          <div id='funcinfo' style={{ borderRadius: '10%', margin: '5px' }}>
            <h3 id='funcname'></h3>
            <h4 id="parametertitle"></h4><p id='parameterslistedout'></p>
            <h4 id="desctitle"></h4><p id='desciption' ></p>
          </div>
        </div>
      </div>
    </div>

  </div >
    ;
}

export default Header;

function fillinfo(info) {
  document.getElementById('funclist').onmouseover = null;
  document.getElementById('funclist').style.height = 0;

  document.getElementById('funcname').textContent = info[0];
  document.getElementById('desciption').textContent = info[2];
  document.getElementById('parameterslistedout').textContent = info[1].toString();
  document.getElementById('parametertitle').textContent = 'Parameters';
  document.getElementById('desctitle').textContent = 'Description';
  document.getElementById('funclist').style.visibility = 'hidden';
  document.getElementById('select').style.backgroundColor = 'white';
}

/*

                <h5 onClick={() => fillinfo(addnodes)}>AddNodes():</h5>
                <h5 onClick={() => fillinfo(graphdesc)}>CreateGraph():</h5>
                <h5 onClick={() => fillinfo(collisiondesc)}>Collision():</h5>
                <h5 onClick={() => fillinfo(mergedesc)}>MergeGraph():</h5>
                <h5 onClick={() => fillinfo(filterdesc)}>FilterGraph():</h5>
                <h5 onClick={() => fillinfo(shortestpathdesc)}>ShortestPath():</h5>
                <h5 onClick={() => fillinfo(getnodesdesc)}>GetNodes():</h5>
                <h5 onClick={() => fillinfo(visdesc)}>Vis():</h5>
                <h5 onClick={() => fillinfo(savedesc)}>Save():</h5>
                <h5 onClick={() => fillinfo(networkx)}>Networkx():</h5>
                <h5 onClick={() => fillinfo(subgraphdesc)}>SubGraph():</h5>
                <h5 onClick={() => fillinfo(semanticgraphdesc)}>SemanticGraph():</h5>

const graphdesc = [
  'CreateGraph()', ['(csv: str = None) -> Graph'],
  "This function creates a new graph object, optionally populated with nodes and edges from a CSV file. It takes an optional parameter csv (string) representing the path to the CSV file containing node data. If no parameter was passed, an empty graph will be created."
]
const semanticgraphdesc = ['SemanticGraph()', [
  "author name",
  "choice",
  "number of papers"
], "The semantic graph function initializes a new graph variable representing the constructed graph structure. If a name is specified, the function accesses Semantic Scholar data associated with the provided name and constructs a graph centered around it, incorporating co-authors as additional nodes. Disambiguation will be applied to ensure accurate retrieval of the targeted person's information. In the case of a CSV file, the function parses it to generate one or more node objects based on the entries. Data originates exclusively from the file itself. If an error arises during graph creation, specific error messages are provided to identify the nature of the issue, whether it's due to an invalid input or difficulties in parsing the CSV file."]
const subgraphdesc = ['SubGraph()', [
  "graph",
  "node"
], "The subgraph function processes an existing graph along with a specified name or node as input. It generates a subgraph centered around the provided name or node, revealing the complete structure of the selected entity. This subgraph facilitates exploration of all nodes connected to the target with shared attributes. Upon execution, the function returns the subgraph, enabling further manipulation or analysis. In the event of an invalid or incorrect graph variable/name input, the function remains inactive and outputs an error message on the REPL to notify the user."]
const getnodesdesc = ['GetNodes()', [
  "graph"
], "The GetNodes function retrieves a list of nodes from a given graph. It simply calls the get_nodes method of the Graph class and returns the resulting list of nodes."]
const collisiondesc = ['Collision()', [
  "graph",
  "graph"
], "The Collision function takes two graphs as input and returns a dictionary where the keys are node names and the values are lists of nodes with that name. This function identifies nodes that exist in both graphs, storing them in the dictionary. If a node name already exists as a key in the dictionary, the corresponding node is appended to the existing list of nodes. After processing both graphs, the function removes any entries where the list of nodes has only one element. Finally, it returns the dictionary containing nodes that collide between the two graphs."]
const visdesc = ['Vis()', ['ntx'],
  "This function accepts an existing graph variable and visually displays the entire graph associated with that object in a new window. Through this visualization, users can observe the relationships and connections, as well as the absence of connections between nodes. If the specified graph variable is invalid or of an incorrect type, the function remains inactive and prompts an error message on the REPL to inform the user."
]
const savedesc =
  ['Save()', ['graph'],
    'This function stores the graph data for session storage, enabling users to preserve their graph structure for future use. If the specified graph does not exist or is of an incorrect type, the function remains inactive, accompanied by an error message on the REPL to inform the user.'
  ]
const filterdesc = [
  'FilterGraph()', ['graph', 'attributetype1', 'attributevalue1', '...'],
  "The filter function accepts a graph variable along with a series of attribute types and their corresponding values (entered as strings) as parameters. Its purpose is to process the nodes in the graph, returning a new graph variable containing nodes that match the provided attribute-value pairs. If the specified graph variable or attribute types/values are invalid or of an incorrect type, the function remains inactive and notifies the user with an error message on the REPL."
]
const shortestpathdesc = [
  'ShortestPath()', ['graph', 'start_attributes', 'end_attributes'],
  "The shortestpath function is designed to determine the most efficient route between two nodes within the graph, considering specific attribute types and their corresponding values for both the starting and ending nodes. This method navigates through the graph's nodes and edges, analyzing the attributes provided to identify the shortest path connecting the nodes of interest. The parameters start_attributes and end_attributes are lists containing tuples of attribute types and their corresponding values for the starting and ending nodes, respectively. If the specified graph variable or attribute types/values are invalid or of an incorrect type, the function remains inactive and notifies the user with an error message on the REPL."
]
const mergedesc = [
  'MergeGraph()', ['graph1', 'graph2'],
  "This function merges two graphs to create a new one based on any nodes with any common attributes. Disambiguation processes will be applied during the merging operation to maintain data accuracy. If no common nodes are found or if either graph is of an incorrect type, the function remains inactive, accompanied by a message on the REPL to inform the user."
]
const addnodes = [
  'AddNodes()', ['graph', 'csv'],
  "The addnodes function expands a previously existing graph by incorporating additional nodes retrieved from a CSV file. It doesn't create a new graph but augments an existing one with new nodes. If the specified graph variable is invalid or of an incorrect type, the function remains inactive and notifies the user with an error message on the REPL."
]
const networkx = [
  'Networkx()', ['graph'],
  "This function accepts a graph and converts it to a networkx object (which can be used for visualization) that it then returns."
]*/
const semanticgraphdesc = [
  'SemanticGraph',
  '(author_name: str, choice: int = 1, numpapers: int = 5) -> Graph',
  "This function generates a graph representing the collaboration network of an author based on Semantic Scholar data. It takes an author's name as a string (author_name), an optional integer choice that determines the particular author to select (default is 1), and an optional integer numpapers representing the number of papers to consider (default is 5)."
]

const addnodesdesc = [
  'AddNodes',
  '(graph: Graph, nodes_list: List[Node]) -> Graph',
  "This function adds nodes to an existing graph object. It takes a graph object (Graph) representing the target graph and a list of nodes_list (list[Node]) representing the nodes to be added to the target graph."
]

const subgraphdesc = [
  'SubGraph',
  '(graph: Graph, chosen_node: Node) -> Graph',
  "This function creates a subgraph from an existing graph centered around a chosen node. It takes a graph object (Graph) representing the original graph and a chosen_node (Node) representing the center node of the subgraph."
]

const filtergraphdesc = [
  'FilterGraph',
  '(graph: Graph, attributes: Dict[str: List[str]] = None, lamb = None) -> Graph',
  "This function filters nodes based on attributes or custom logic. It takes a graph object (graph), an optional dictionary of attributes (attributes), and an optional function (lamb). If attributes are given, it returns a new graph with nodes matching those attributes. If the optional function is provided, it filters nodes based on custom logic."
]

const collisiondesc = [
  'Collision',
  '(graph1: Graph, graph2: Graph, list_return: bool = False) -> Optional[List[List[Node]],  Dict[str: List[Node]]',
  "This function identifies nodes in two graphs that have the same name. It takes two graph objects (graph1 and graph2) and an optional list_return (boolean) parameter indicating whether to return a list of collisions or a dictionary of collisions."
]

const collisionlistdesc = [
  'CollisionList',
  '(Dict[str: List[Node]) -> Optional[List[Tuple[Node]]]',
  "This function returns a list of collision pairs identified by the Collision() function. It takes a dictionary of names paired with a list of nodes with that name."
]

const mergegraphdesc = [
  'MergeGraph',
  '(graph1: Graph, graph2: Graph, merge_list: List[Tuple[Node, Node]]) -> Graph',
  "This function merges nodes from two graphs based on a specified merge list. It takes two graph objects (graph1 and graph2) and an optional merge_list (list) parameter specifying the nodes to be merged and returns the merged graph."
]

const getnodesdesc = [
  'GetNodes',
  '(graph: Graph) -> List[Node]',
  "This function retrieves a list of nodes from a graph. It takes a graph object (Graph) as input."
]

const nodefromgraphdesc = [
  'NodeFromGraph',
  '(graph: Graph, name: str) -> Optional[Node, List[Node]]',
  "This function retrieves a node from a graph based on its name. It takes a graph object (Graph) and a name (str) representing the name of the node. If only one node in the graph has that name, it returns that node. Otherwise, it returns a list of nodes with that name."
]

const namesingraphdesc = [
  'NamesInGraph',
  '(graph: Graph) -> List[str]',
  "This function returns a sorted list of unique node names present in a graph. It takes a graph object (Graph) as input."
]

const shortestpathdesc = [
  'ShortestPath',
  '(source: Node, target: Node, graph: Graph) -> List[Node]',
  "This function calculates the shortest path between two nodes in a graph. It takes three parameters: a source node (Node), a target node (Node), and a graph object (Graph) and returns a list of the path of the nodes."
]

const visdesc = [
  'Vis',
  '(graph: Graph) -> None',
  "This function generates a visualization of a graph using the Pyvis library. It takes a graph object (Graph) as input."
]

const updatenodeattributesdesc = [
  'UpdateNodeAttributes',
  '(graph: Graph, node: Node, attributes: Dict[str, List[str]]) -> None',
  "This function updates the attributes of a node in a graph. It takes three parameters: a graph object (Graph), a node (Node) belonging to the passed graph object whose attributes are to be updated, and an attributes (dict) parameter representing the new attributes."
]

const nodecentralitydesc = [
  'NodeCentrality',
  '(graph: Graph, node: Node) -> float',
  "This function calculates the centrality of a node in a graph. It takes two parameters: a graph object (Graph) and a node (Node) whose centrality is to be calculated."
]

const savedatadesc = [
  'SaveData',
  '(nodes: List[Node], filePath: str) -> None',
  "This function saves node and relationship data from a list of nodes to a CSV file. It takes two parameters: a list of nodes and a filePath (str) representing the path to save the CSV file."
]


const functionDescriptions = [
  semanticgraphdesc,
  addnodesdesc,
  subgraphdesc,
  filtergraphdesc,
  collisiondesc,
  collisionlistdesc,
  mergegraphdesc,
  getnodesdesc,
  nodefromgraphdesc,
  namesingraphdesc,
  shortestpathdesc,
  visdesc,
  updatenodeattributesdesc,
  nodecentralitydesc,
  savedatadesc
];
