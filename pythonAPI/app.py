from flask import Flask, request, jsonify, send_file
import time
import sys
import os
import uuid
import global_vars
from io import StringIO
from flask_cors import CORS


sys.path.append(os.getcwd() + '/finalized_backend')
from AuthorNode import *
from EdgeClass import *
from Functions import *
from GraphClass import *
from NodeClass import *
from parse import parseData
from SemanticScholarFuncs import *

app = Flask(__name__, static_url_path='/lib/bindings')
CORS(app, origins=['http://localhost:3000'], methods=['GET', 'POST'], expose_headers='Access-Control-Allow-Origin')


# It will contain the current command run and all the previous commands ran for that instance of the site
@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json['code']

    #parts = code.strip().split('\n')
    
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
    filepath = f"{os.getcwd()}/{var_name}.html"
    # return ERROR HERE for if graph name is not contained
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='text/html')
    else:
        return jsonify({'output': None, 'error': f"No graph with the name {var_name} exists."})
    
@app.route('/save_graph', methods=['GET'])
def save_graph():
    var_name = request.args.get('varName')
    session_id = request.headers.get('session')
    filepath = f"{os.getcwd()}/csv_list/{session_id}/{var_name}.csv"
    # return ERROR HERE for if graph name is not contained
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=f'{var_name}.csv', mimetype='text/csv')
    else:
        return jsonify({'output': None, 'error': f"No graph with the name {var_name} exists."})
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['file']
    csv_name = request.form['csvName'].lower()
    # get session id from header
    session_id = request.headers.get('session')
    # if path does not exist for csv and session, make it
    filepath = f'{os.getcwd()}/csv_list/{session_id}'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    csv = f'{filepath}/{csv_name}'

    base, ext = os.path.splitext(csv_name)
    counter = 1
    while os.path.exists(csv):
        csv = f"{filepath}/{base} ({counter}){ext}"
        counter += 1
    file.save(csv)
    global_vars.session_id = session_id
    try:
        parseData(csv)
    except Exception as e:
        return jsonify({'output': None, 'error': str(e)})
    return {'message': 'File uploaded successfully'}, 200

@app.route('/initiate', methods=['GET'])
def initiate():
    session_id = str(uuid.uuid4())
    return jsonify({'session_id': session_id}), 200

if __name__ == '__main__':
    app.run(debug=True)