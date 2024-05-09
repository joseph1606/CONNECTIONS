import "./Header.css";
import i from "./media/information-button.png"
import logo from "./media/download.png"
import house from "./media/house.png"

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
      <div style={{ display: 'flex', backgroundColor: "white", margin: '5px', border: '2px solid grey', borderRadius: '15px', fontFamily: 'bold', marginLeft: '.5vw', minWidth: '300px', alignItems: 'center', minHeight: '5vh' }}>
        <img src={logo} alt="logo" style={{ padding: '5px', height: '6vh' }} />
        <h1 id='title' style={{ color: 'black', width: '9.5vw', fontSize: '2.5vh' }}>Connections</h1>
      </div>
      <div id="info" style={{ border: '0px', position: 'absolute', zIndex: 3, width: '25vw', maxWidth: '25vw', right: 0 }}>
        <img id='i' src={i} alt="Info" onMouseOver={popup} onMouseLeave={cheerdown} />
        <div id="functions" style={{ visibility: 'hidden', display: 'none' }} onMouseOver={popup} onMouseLeave={cheerdown}>
          <h1 >Functions</h1>
          <div style={{ height: 'fit-content' }} onMouseLeave={funccheerdown}>
            <h4 onMouseOver={funcpopup} id='select' style={{ outline: '2px solid grey', marginLeft: '10%', marginRight: '10%', backgroundColor: 'white' }}>Select Function:</h4>
            <div id="funclist" onMouseOver={funcpopup} style={{ visibility: 'hidden', backgroundColor: 'whitesmoke', border: '1px solid grey', padding: '2px', height: '150%', position: 'absolute', width: '98%', left: '1%' }}>
              <div className="funclistitem">
                {functionDescriptions.map((funcdesc, index) => (
                  <h5 key={funcdesc[0]} onClick={() => fillinfo(funcdesc)}>{funcdesc[0]}</h5>
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
      <a href="http://vegetable.cs.umd.edu:3001/" style={{ position: 'absolute', right: '0', zIndex: 4 }} target="_blank" rel="noreferrer"><img src={house} style={{ height: '7vh', width: '7vh' }} alt="" /></a>
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
  'Save',
  '(graph: Graph) -> None',
  "This function saves node and relationship data from a graph to a CSV file. It takes one parameter: a graph object (Graph)."
]
const creategraphdesc = [
  'CreateGraph',
  '(csv: str = None) -> Graph',
  "This function creates a new graph object, optionally populated with nodes and edges from a CSV file. It takes an optional parameter csv (string) representing the path to the CSV file containing node data. If no parameter was passed, an empty graph will be created."
]


const functionDescriptions = [
  addnodesdesc,
  creategraphdesc,
  collisiondesc,
  collisionlistdesc,
  filtergraphdesc,
  getnodesdesc,
  mergegraphdesc,
  namesingraphdesc,
  nodecentralitydesc,
  nodefromgraphdesc,
  savedatadesc,
  semanticgraphdesc,
  shortestpathdesc,
  subgraphdesc,
  updatenodeattributesdesc,
  visdesc
];
