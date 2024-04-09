# New Connections Use Guide

This guide will walk you through currently active functions to be used in our REPL. 

## Website

http://vegetable.cs.umd.edu:3000/

## Functions

1. MergeGraph:

    Description: 
    Merges two input graphs into a single graph. It allows merging specific nodes from each graph based on the provided merge_list. Merge_list is a list that contains tuples of nodes from the two graphs. Nodes in tuples are merged together in the new graph. Any node not in merge_list will not be merged with any other node. If no merge list is provided, it will not merge any nodes and all the nodes from both graphs will be added to the new graph.

    Usage Prototype/Example:

   ```
   merged_graph = MergeGraph(graph1, graph2, [(node1_graph1, node2_graph2), (node3_graph1, node4_graph2)])
   ```
   
2. Navigate to the cloned directory:

   ```
   cd connections
   ```
   
3. Create a virtual environment:

   ```
   python3 -m venv venv
   ```
   
4. Activate the virtual environment:

   ```
   source venv/bin/activate
   ```
   
5. Install the required packages:

   ```
   pip install -r requirements.txt
   ```
   
6. Set the environment variables:

   ```
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```
   
7. Run the app:

   ```
   flask run
   ```

8. Access the app by opening a web browser and navigating to `http://localhost:5000`.

That's it! You should now have the Flask app up and running on your local machine.
