import "./Header.css";
import i from "./media/information-button.png"
import logo from "./media/download.png"

function popup() {
  document.getElementById('functions').style.visibility = 'visible'

};
function cheerdown() {
  document.getElementById('functions').style.visibility = 'hidden'
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
      <div id="info" style={{ border: '0px', position: 'absolute', zIndex: 1, width: '25vw', maxWidth: '25vw', right: 0 }}>
        <img id='i' src={i} alt="Info" onMouseOver={popup} onMouseLeave={cheerdown} />
        <div id="functions" style={{ visibility: 'hidden' }} onMouseOver={popup} onMouseLeave={cheerdown}>
          <h1>Functions</h1>
          <br />
          <div style={{ height: 'fit-content' }} onMouseLeave={funccheerdown}>
            <h4 onMouseOver={funcpopup} id='select' style={{ outline: '2px solid grey', marginLeft: '10%', marginRight: '10%', backgroundColor: 'white' }}>Select Function:</h4>
            <div id="funclist" onMouseOver={funcpopup} style={{ visibility: 'hidden', backgroundColor: 'whitesmoke', border: '1px solid grey', padding: '2px', height: '100%', position: 'absolute', width: '98%', left: '1%' }}>
              <div className="funclistitem">
                <h5 onClick={() => fillinfo(addnodes)}>AddNodes():</h5>
                {/*<h5 onClick={() => fillinfo(addnodehelper)}>AddNodeHelper():</h5>*/}
                <h5 onClick={() => fillinfo(graphdesc)}>CreateGraph():</h5> </div>
              <h5 onClick={() => fillinfo(semanticgraphdesc)}>SemanticGraph():</h5>
              <h5 onClick={() => fillinfo(subgraphdesc)}>SubGraph():</h5>
              <h5 onClick={() => fillinfo(collisiondesc)}>Collision():</h5>
              <h5 onClick={() => fillinfo(mergedesc)}>MergeGraph():</h5>
              <h5 onClick={() => fillinfo(filterdesc)}>FilterGraph():</h5>
              <h5 onClick={() => fillinfo(shortestpathdesc)}>ShortestPath():</h5>
              <h5 onClick={() => fillinfo(getnodesdesc)}>GetNodes():</h5>
              <h5 onClick={() => fillinfo(visdesc)}>Vis():</h5>
              <h5 onClick={() => fillinfo(savedesc)}>Save():</h5>
              <h5 onClick={() => fillinfo(networkx)}>Networkx():</h5>
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

const graphdesc = [
  'CreateGraph()', ['filename.csv'],
  "The CreateGraph function constructs a graph object. If a CSV file is provided as input, the function generates nodes based on the CSV data. It first checks if the CSV file exists and then parses the data, creating nodes accordingly. If the CSV contains pairs of names, it creates nodes for each pair. Otherwise, it creates nodes for each entry. After creating the nodes, the function generates colors for the graph before returning it. In case of no input, the function creates an empty graph, allowing users to add nodes using the AddNodes method. If an invalid CSV name is provided, the function raises a ValueError."
]
const semanticgraphdesc = ['SemanticGraph()', [
  "author name",
  "choice",
  "number of papers"
],   "The semantic graph function initializes a new graph variable representing the constructed graph structure. If a name is specified, the function accesses Semantic Scholar data associated with the provided name and constructs a graph centered around it, incorporating co-authors as additional nodes. Disambiguation will be applied to ensure accurate retrieval of the targeted person's information. In the case of a CSV file, the function parses it to generate one or more node objects based on the entries. Data originates exclusively from the file itself. If an error arises during graph creation, specific error messages are provided to identify the nature of the issue, whether it's due to an invalid input or difficulties in parsing the CSV file."]
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
const addnodehelper = [
  'AddNodeHelper()', ['graph', 'node'],
  "This function accepts a graph, single node, and attribute of type dictionary and appends the node to the graph with the appropriate relationship, then returns the graph."
]
const networkx = [
  'Networkx()', ['graph'],
  "This function accepts a graph and converts it to a networkx object (which can be used for visualization) that it then returns."
]
