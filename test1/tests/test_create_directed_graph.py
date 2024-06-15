import pytest
from src.create_directed_graph import create_directed_graph

def test_create_directed_graph():
    # 测试用例1：空字符串
    text1 = ""
    graph1 = create_directed_graph(text1)
    assert len(graph1.nodes()) == 0
    assert len(graph1.edges()) == 0

    # 测试用例2：不包含有效单词的字符串
    text2 = ".,!?;:"
    graph2 = create_directed_graph(text2)
    assert len(graph2.nodes()) == 0
    assert len(graph2.edges()) == 0

    # 测试用例3：包含单个单词的字符串
    text3 = "hello"
    graph3 = create_directed_graph(text3)
    assert len(graph3.nodes()) == 1
    assert len(graph3.edges()) == 0

    # 测试用例4：包含多个不同单词的字符串
    text4 = "hello world"
    graph4 = create_directed_graph(text4)
    assert len(graph4.nodes()) == 2
    assert len(graph4.edges()) == 1
    assert graph4["hello"]["world"]["weight"] == 1

    # 测试用例5：包含重复单词的字符串
    text5 = "hello world hello"
    graph5 = create_directed_graph(text5)
    assert len(graph5.nodes()) == 2
    assert len(graph5.edges()) == 2
    assert graph5["hello"]["world"]["weight"] == 1
    assert graph5["world"]["hello"]["weight"] == 1

    # 测试用例6：包含特殊字符和数字的字符串
    text6 = "hello world! 123 world hello."
    graph6 = create_directed_graph(text6)
    assert len(graph6.nodes()) == 3
    assert len(graph6.edges()) == 4
    assert graph6["hello"]["world"]["weight"] == 1
    assert graph6["world"]["123"]["weight"] == 1
    assert graph6["123"]["world"]["weight"] == 1

    # 边界值测试1：长度为1的字符串
    text7 = "a"
    graph7 = create_directed_graph(text7)
    assert len(graph7.nodes()) == 1
    assert len(graph7.edges()) == 0

    # 边界值测试2：长度为2的字符串
    text8 = "a b"
    graph8 = create_directed_graph(text8)
    assert len(graph8.nodes()) == 2
    assert len(graph8.edges()) == 1
    assert graph8["a"]["b"]["weight"] == 1

    # 边界值测试3：非常长的字符串
    text9 = "a " * 1000 + "b"
    graph9 = create_directed_graph(text9)
    assert len(graph9.nodes()) == 2
    assert len(graph9.edges()) == 2
    assert graph9["a"]["a"]["weight"] == 999
    assert graph9["a"]["b"]["weight"] == 1
