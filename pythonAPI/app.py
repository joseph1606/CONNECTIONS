from flask import Flask, request, jsonify, send_file
import subprocess
import time
import sys
import os
import re
from io import StringIO
from pyvis.network import Network
import networkx as nx
from flask_cors import CORS

import requests
from AutherNode import AuthorNode, PaperNode

sys.path.append('/Users/andrewtimmer/repo_connection/new_connections/pythonAPI/finalized_backend')
# from Functions import CreateGraph, AddNodes
from Functions import CreateGraph, AddNodes, Vis, Networkx
from GraphClass import Graph
'''
from back_end.new_graphclass.GraphClass.Tester.Joel.Functions import CreateGraph, AddNodes
from back_end.new_graphclass.GraphClass.Tester.Joel.Graph import input_received, Graph'''

app = Flask(__name__, static_url_path='/lib/bindings')
CORS(app, origins=['http://localhost:3000'], methods=['GET', 'POST'], allow_headers=['Content-Type'])


def fetch_author(query):
    url = f"https://api.semanticscholar.org/graph/v1/author/search?query={query}&fields=name,aliases,url,papers.title,papers.year,papers.authors&limit=5"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
def display_author_options(aliases):
    list_of_aliases = []
    if aliases["total"] > 0:
        for i, author in enumerate(aliases["data"]):
            name = author.get('name')
            url = author.get('url')
            print(f"{i + 1}. {name} ({url})")
            list_of_aliases.append(name)
            
    return list_of_aliases

def search(name):
    disamb = fetch_author(name)
    display_author_options(disamb)

def parse_author_data(author_data):
    author_nodes = []
    if author_data["total"] > 0:
        for author in author_data["data"]:
            name = author.get("name")
            aliases = author.get("aliases")
            authorId = author.get("authorId")
            url = author.get("url")
            papers = []
            if "papers" in author:
                paper_count = 0  # Counter to track the number of papers processed
                for paper in author["papers"]:
                    if paper_count >= 2:
                        break  # Exit loop if ten papers have been processed
                    title = paper.get("title")
                    year = paper.get("year")
                    authors = []
                    authorIds = []
                    if "authors" in paper:
                        for coauthor in paper["authors"]:
                            authors.append(coauthor.get("name"))
                            authorIds.append(coauthor.get("authorId"))
                    papers.append(PaperNode(title, year, authors, authorIds))
                    paper_count += 1
            author_node = AuthorNode(name, None, aliases, authorId, url, papers)
            author_nodes.append(author_node)
    return author_nodes

def makeAuthor(name, number):
    disamb = fetch_author(name)
    list_of_aliases = display_author_options(disamb)

    # parts[-1] will be the index
    selected_author = list_of_aliases[number-1]

    if selected_author:
        author_nodes = parse_author_data(disamb)
        selected_author_node = None
        for author in author_nodes:
            if author.name == selected_author:
                selected_author_node = author
                break
        
        if selected_author_node:
          #print_author_details(selected_author_node)
          #print(selected_author_node.name)
          #print(type(selected_author_node))
          return selected_author_node  
        else:
            print("Selected author not found in the retrieved data.")

    else:
        print("No data found. Try again")

def create_coauthor_nodes(author_node):
    coauthor_nodes = []  # List to store coauthor nodes
    # Iterate through each paper of the author
    for paper in author_node.papers:
        r = requests.post('https://api.semanticscholar.org/graph/v1/author/batch',
            params={'fields': 'name,aliases,authorId,url'},
            json={"ids":paper.authorIds}
        )
        coauthors_data = r.json()
        for coauthor_data in coauthors_data:
            if coauthor_data['name'] != author_node.name:
                coauthor_node = AuthorNode(
                    name=coauthor_data['name'],
                    attributes=None,
                    aliases=coauthor_data['aliases'],
                    authorId=coauthor_data['authorId'],
                    url=coauthor_data['url'],
                    papers=[]  # Assuming we don't have papers for coauthors initially
                )
            coauthor_nodes.append(coauthor_node)
    return coauthor_nodes

def generate_author_list(author_name):
    author_list = []
    author = makeAuthor(author_name)
    if author:
        author_list.append(author)
        coauthors = create_coauthor_nodes(author)
        author_list.extend(coauthors)  # Extend the list with coauthors
        for each in author_list:
            print(each.name)
    else:
        print("Author not found.")

def print_author_details(auth):
            print("Name:", auth.name)
            print("Aliases:", ", ".join(auth.aliases))
            print("URL:", auth.url)
            if auth.papers:
                print("Papers:")
                for paper in auth.papers:
                    print("\tTitle:", paper.title)
                    print("\tYear:", paper.year)
                    print("\tAuthors:")
                    for author in paper.authors:
                        print(f"\t\tName: {author[0]}, Author ID: {author[1]}")
                    print()
            else:
                print("No papers found")



'''def create1Graph():
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
    return nt'''


def displayGraph(fileName):
    # this is what should be run when a graph is created
    '''nt.from_nx(nx_graph)
    graph_name = global_graph_name + '.html'
    nt.show(graph_name)'''
    cwd = os.getcwd()
    filepath = cwd + "/" + fileName
    with open(filepath, 'r') as file:
        html_content = file.read()
    return html_content

def is_number(text):
    # Define the regular expression pattern to match a number from 0 to 9
    pattern = r"^[0-9]$"

    # Use re.match to search for the pattern in the text
    match = re.match(pattern, text)

    # If there is a match, return True, else return False
    return bool(match)

# It will contain the current command run and all the previous commands ran for that instance of the site
@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json['code']

    parts = code.strip().split('\n')

    # need some way to indicate the disambiugation process is still ongoing
    '''if parts[-2].find("CreateGraph('csv')") != -1:
        if is_number(parts[-1]):
            input_received.set()
        else:
            return jsonify({'output': None, 'error': "Invalid input. Please enter a valid number."})'''
       
        
    # checks if most recent code line is something like g = CreateGraph("James")
    '''if len(parts) > 1 and parts[-2].find("CreateGraph") != -1 and parts[-2].find("csv") == -1:
        # if most recent line is a number btwn 0 to 9 OR keyword 'next'
        name = parts[-2][parts[-2].index("(") + 2:len(parts[-2]) - 1]
        if is_number(parts[-1]):
            # select author from list of authors with parts[-1]
            makeAuthor(int(parts[-1]), name)
        else:
            return jsonify({'output': None, 'error': "Invalid input. Please enter a valid number."})
        global global_graph_name
        global_graph_name = (parts[-1].split("=")[0]).strip()
        if not global_graph_name:
            return jsonify({'output': None, 'error': str(global_graph_name + ": Not a valid graph name")})'''

    
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
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['file']
    # Do something with the file, e.g., save it to disk
    # errorChecking and check for errors before saving, change name of csv file
    file.save('/Users/andrewtimmer/repo_connection/new_connections/pythonAPI/back_end/new_graphclass/GraphClass/Tester/Joel/data.csv')
    return {'message': 'File uploaded successfully'}, 200

if __name__ == '__main__':
    app.run(debug=True)