import re
import networkx as nx
from collections import Counter



def find_shortest_path(graph, word1, word2):
    if word1 not in graph or word2 not in graph:
        return None, None
    try:
        length, path = nx.single_source_dijkstra(graph, word1, word2)
        return length, path
    except nx.NetworkXNoPath:
        return None, None