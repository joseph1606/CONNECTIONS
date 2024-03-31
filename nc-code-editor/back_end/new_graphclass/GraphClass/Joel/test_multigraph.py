from Graph import Graph

# Create a new graph
graph = Graph()

# Add a node with initial attributes
graph.add_node("A", {"color": "red", "shape": "circle"})

# Print the initial attributes of node "A"
print("Initial attributes of node 'A':", graph.nxGraph.nodes["A"])

# Update the attributes of node "A"
graph.add_node("A", {"color": "blue", "size": "large", "shape":"rectangle"})

# Print the updated attributes of node "A"
print("Updated attributes of node 'A':", graph.nxGraph.nodes["A"])
