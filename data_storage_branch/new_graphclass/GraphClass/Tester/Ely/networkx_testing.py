import networkx as nx
import matplotlib.pyplot as plt

G = nx.MultiGraph()
G.add_node(1)

G.add_edge(1, 2)
e = (2, 3)
G.add_edge(*e)

G.add_edge(1, 2)
G.add_node("spam")  # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, "m")
G.add_edge("spam", "s")

nx.draw(G, with_labels=True, font_weight="bold")
plt.show()
