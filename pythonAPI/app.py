from flask import Flask, request, jsonify, send_file
import subprocess
import time
import sys
import os
from io import StringIO
from pyvis.network import Network
import networkx as nx
from flask_cors import CORS

app = Flask(__name__, static_url_path='/lib/bindings')
CORS(app, origins=['http://localhost:3000'], methods=['GET', 'POST'], allow_headers=['Content-Type'])


def createGraph():
    nx_graph = nx.cycle_graph(10)
    nx_graph.nodes[1]['title'] = 'Number 1'
    nx_graph.nodes[1]['group'] = 1
    nx_graph.nodes[3]['title'] = 'I belong to a different group!'
    nx_graph.nodes[3]['group'] = 10
    nx_graph.add_node(20, size=20, title='couple', group=2)
    nx_graph.add_node(21, size=15, title='couple', group=2)
    nx_graph.add_edge(20, 21, weight=5)
    nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)
    nt = Network('500px', '500px')
    # populates the nodes and edges data structures
    nt.from_nx(nx_graph)
    graph_name = global_graph_name + '.html'
    nt.show(graph_name)

def displayGraph(fileName):
    cwd = os.getcwd()
    filepath = cwd + "/" + fileName
    with open(filepath, 'r') as file:
        html_content = file.read()
    return html_content

# It will contain the current command run and all the previous commands ran for that instance of the site
@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json['code']

    parts = code.strip().split('\n')
    if parts[-1].find("createGraph()") != -1:
        global global_graph_name
        global_graph_name = (parts[-1].split("=")[0]).strip()
        if not global_graph_name:
            return jsonify({'output': None, 'error': str(global_graph_name + ": Not a valid graph name")})
    
    output = StringIO()  # Create StringIO object to capture output
    sys.stdout = output   # Redirect stdout to StringIO object
    
    start_time = time.time()
    try:
        # Execute code with custom function
        exec(code)
        runtime = time.time() - start_time
        output_str = output.getvalue()  # Get contents of StringIO object
        return jsonify({'output': output_str, 'runtime': runtime, 'error': None})
    except Exception as e:
        runtime = time.time() - start_time
        return jsonify({'output': None, 'runtime': runtime, 'error': str(e)})
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout to its original value

@app.route('/get_graph', methods=['GET'])
def get_graph():
    var_name = request.args.get('varName')
    cwd = os.getcwd()
    filepath = cwd + "/" + var_name + ".html"
    # return ERROR HERE for if graph name is not contained
    try: 
        os.path.exists(filepath)
        return send_file(filepath, mimetype='text/html')
    except Exception as e:
        return jsonify({'output': None, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)