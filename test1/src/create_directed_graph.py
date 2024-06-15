import re
import networkx as nx
from collections import Counter

def create_directed_graph(text):
    words = re.findall(r'\b\w+\b', text.lower())
    graph = nx.DiGraph()
    if len(words) < 2:
        # If there's less than 2 words, no edges can be created
        for word in words:
            graph.add_node(word)
        return graph
    
    edge_weights = Counter(zip(words, words[1:]))
    for (a, b), weight in edge_weights.items():
        graph.add_edge(a, b, weight=weight)
    return graph
