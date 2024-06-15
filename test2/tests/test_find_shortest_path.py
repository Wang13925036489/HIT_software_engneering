import pytest
from src.find_shortest_path import find_shortest_path
import networkx as nx
from collections import Counter
import re

def create_directed_graph(text):
    words = re.findall(r'\b\w+\b', text.lower())
    graph = nx.DiGraph()
    edge_weights = Counter(zip(words, words[1:]))
    for (a, b), weight in edge_weights.items():
        graph.add_edge(a, b, weight=weight)
    return graph

def test_find_shortest_path():
    # 测试用例1：图中不包含 word1 或 word2
    text1 = "hello world"
    graph1 = create_directed_graph(text1)
    length, path = find_shortest_path(graph1, "hello", "universe")
    assert length is None
    assert path is None

    # 测试用例2：图中包含 word1 和 word2，且存在路径
    text2 = "hello world this is a test"
    graph2 = create_directed_graph(text2)
    length, path = find_shortest_path(graph2, "hello", "test")
    assert length == 5  # hello -> world -> this -> is -> a -> test
    assert path == ['hello', 'world', 'this', 'is', 'a', 'test']

    # 测试用例3：图中包含 word1 和 word2，但不存在路径
    text3 = "hello world. test case."
    graph3 = create_directed_graph(text3)
    length, path = find_shortest_path(graph3, "case", "hello")
    assert length is None
    assert path is None

