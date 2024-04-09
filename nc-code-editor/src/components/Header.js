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
      <div style={{ display: 'flex', backgroundColor: "white", margin: '5px', border: '2px solid grey', borderRadius: '15px', fontFamily: 'bold', marginLeft: '.5vw', minWidth: '19vw' }}>
        <img src={logo} alt="logo" style={{ padding: '5px' }} />
        <h1 id='title' style={{ color: 'black', width: '9.5vw', height: 'fit-contents', marginTop: '1.25vh' }}>Connections</h1>

      </div>
      <div id="info" style={{ border: '0px', marginLeft: '70vw', position: 'relative', zIndex: 1, width: '30vw', maxWidth: '30vw' }}>
        <img id='i' src={i} alt="Info" onMouseOver={popup} onMouseLeave={cheerdown} />
        <div id="functions" style={{ visibility: 'hidden' }} onMouseOver={popup} onMouseLeave={cheerdown}>
          <h1>Functions</h1>
          <br />
          <div style={{ height: 'fit-content' }} onMouseLeave={funccheerdown}>
            <h4 onMouseOver={funcpopup} id='select' style={{ outline: '2px solid grey', marginLeft: '10%', marginRight: '10%', backgroundColor: 'white' }}>Select Function:</h4>
            <div id="funclist" onMouseOver={funcpopup} style={{ visibility: 'hidden', backgroundColor: 'whitesmoke', border: '1px solid grey', padding: '2px', height: '100%', position: 'absolute', width: '98%', left: '1%' }}>
              <div className="funclistitem"><h5 onClick={() => fillinfo(adddesc)}>add():</h5>
                <h5 onClick={() => fillinfo(graphdesc)}>graph():</h5> </div>
              <h5 onClick={() => fillinfo(subgraphdesc)}>subgraph():</h5>
              <h5 onClick={() => fillinfo(visdesc)}>vis():</h5>
              <h5 onClick={() => fillinfo(mergedesc)}>merge(graph1, graph2):</h5>
              <h5 onClick={() => fillinfo(savedesc)}>save():</h5>
              <h5 onClick={() => fillinfo(filterdesc)}>filter(graph,...):</h5>
              <h5 onClick={() => fillinfo(shortestpathdesc)}>shortestpath(graph, start_attributes, end_attributes):</h5>
            </div>
          </div>
          <div id='info' style={{ borderRadius: '10%', margin: '5px' }}>
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
  //document.getElementById('info').style.border = '1px solid grey';

  document.getElementById('funcname').textContent = info[0];
  document.getElementById('desciption').textContent = info[2];
  document.getElementById('parameterslistedout').textContent = info[1].toString();
  document.getElementById('parametertitle').textContent = 'Parameters';
  document.getElementById('desctitle').textContent = 'Description';
  document.getElementById('funclist').style.visibility = 'hidden';
  document.getElementById('select').style.backgroundColor = 'white';
}

const graphdesc = [
  'graph()', ['name/filename.csv'],
  "The graph function initializes a new graph variable representing the constructed graph structure. If a name is specified, the function accesses Semantic Scholar data associated with the provided name and constructs a graph centered around it, incorporating co-authors as additional nodes. Disambiguation will be applied to ensure accurate retrieval of the targeted person's information. In the case of a CSV file, the function parses it to generate one or more node objects based on the entries. Data originates exclusively from the file itself. If an error arises during graph creation, specific error messages are provided to identify the nature of the issue, whether it's due to an invalid input or difficulties in parsing the CSV file."
]
const subgraphdesc = ['subgraph()', [
  "graph",
  "name"
], "The subgraph function processes an existing graph along with a specified name or node as input. It generates a subgraph centered around the provided name or node, revealing the complete structure of the selected entity. This subgraph facilitates exploration of all nodes connected to the target with shared attributes. Upon execution, the function returns the subgraph, enabling further manipulation or analysis. In the event of an invalid or incorrect graph variable/name input, the function remains inactive and outputs an error message on the REPL to notify the user."]
const visdesc = ['vis()', ['graph'],
  "This function accepts an existing graph variable and visually displays the entire graph associated with that object in a new window. Through this visualization, users can observe the relationships and connections, as well as the absence of connections between nodes. If the specified graph variable is invalid or of an incorrect type, the function remains inactive and prompts an error message on the REPL to inform the user."
]
const savedesc =
  ['save()', ['graph'],
    'This function stores the graph data for session storage, enabling users to preserve their graph structure for future use. If the specified graph does not exist or is of an incorrect type, the function remains inactive, accompanied by an error message on the REPL to inform the user.'
  ]
const adddesc = [
  'add()', ['graph', 'filename.csv'],
  "The add function expands a previously existing graph by incorporating additional nodes retrieved from a CSV file. It doesn't create a new graph but augments an existing one with new nodes. If the specified graph variable is invalid or of an incorrect type, the function remains inactive and notifies the user with an error message on the REPL."
]
const filterdesc = [
  'filter()', ['graph', 'attributetype1', 'attributevalue1', '...'],
  "The filter function accepts a graph variable along with a series of attribute types and their corresponding values (entered as strings) as parameters. Its purpose is to process the nodes in the graph, returning a new graph variable containing nodes that match the provided attribute-value pairs. If the specified graph variable or attribute types/values are invalid or of an incorrect type, the function remains inactive and notifies the user with an error message on the REPL."
]
const shortestpathdesc = [
  'shortestpath()', ['graph', 'start_attributes', 'end_attributes'],
  "The shortestpath function is designed to determine the most efficient route between two nodes within the graph, considering specific attribute types and their corresponding values for both the starting and ending nodes. This method navigates through the graph's nodes and edges, analyzing the attributes provided to identify the shortest path connecting the nodes of interest. The parameters start_attributes and end_attributes are lists containing tuples of attribute types and their corresponding values for the starting and ending nodes, respectively. If the specified graph variable or attribute types/values are invalid or of an incorrect type, the function remains inactive and notifies the user with an error message on the REPL."
]
const mergedesc = [
  'merge()', ['graph1', 'graph2'],
  "This function merges two graphs to create a new one based on any nodes with any common attributes. Disambiguation processes will be applied during the merging operation to maintain data accuracy. If no common nodes are found or if either graph is of an incorrect type, the function remains inactive, accompanied by a message on the REPL to inform the user."
]