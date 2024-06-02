import sys
import os
import re
import random
from collections import defaultdict, Counter
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QMessageBox

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def create_directed_graph(text):
    words = re.findall(r'\b\w+\b', text.lower())
    graph = nx.DiGraph()
    edge_weights = Counter(zip(words, words[1:]))
    for (a, b), weight in edge_weights.items():
        graph.add_edge(a, b, weight=weight)
    return graph

def draw_graph(graph, shortest_path=None):
    pos = nx.spring_layout(graph)
    edge_labels = {(u, v): d['weight'] for u, v, d in graph.edges(data=True)}
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', arrows=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    if shortest_path:
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='r', width=2)
    
    plt.show()

def find_bridge_words(graph, word1, word2):
    if word1 not in graph or word2 not in graph:
        return None
    bridge_words = [word3 for word3 in graph[word1] if word2 in graph[word3]]
    return bridge_words

def generate_new_text(graph, new_text):
    words = re.findall(r'\b\w+\b', new_text.lower())
    result = []
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        result.append(word1)
        bridge_words = find_bridge_words(graph, word1, word2)
        if bridge_words:
            bridge_word = random.choice(bridge_words)
            result.append(bridge_word)
    result.append(words[-1])
    return ' '.join(result)

def find_shortest_path(graph, word1, word2):
    if word1 not in graph or word2 not in graph:
        return None, None
    try:
        length, path = nx.single_source_dijkstra(graph, word1, word2)
        return length, path
    except nx.NetworkXNoPath:
        return None, None

def random_walk(graph):
    node = random.choice(list(graph.nodes))
    visited_edges = set()
    walk = []
    while True:
        neighbors = list(graph[node])
        if not neighbors or (node, neighbors[0]) in visited_edges:
            break
        walk.append(node)
        next_node = random.choice(neighbors)
        visited_edges.add((node, next_node))
        node = next_node
    walk.append(node)
    return walk

class TextToGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph = None
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Text to Graph')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        self.load_button = QPushButton('Load Text File', self)
        self.load_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_button)

        self.draw_button = QPushButton('Draw Graph', self)
        self.draw_button.clicked.connect(self.draw_graph)
        layout.addWidget(self.draw_button)

        self.bridge_word_label = QLabel('Find Bridge Words:', self)
        layout.addWidget(self.bridge_word_label)

        self.word1_input = QLineEdit(self)
        self.word1_input.setPlaceholderText('Word 1')
        layout.addWidget(self.word1_input)

        self.word2_input = QLineEdit(self)
        self.word2_input.setPlaceholderText('Word 2')
        layout.addWidget(self.word2_input)

        self.find_bridge_button = QPushButton('Find Bridge Words', self)
        self.find_bridge_button.clicked.connect(self.find_bridge_words)
        layout.addWidget(self.find_bridge_button)

        self.new_text_label = QLabel('Generate New Text:', self)
        layout.addWidget(self.new_text_label)

        self.new_text_input = QLineEdit(self)
        self.new_text_input.setPlaceholderText('Enter new text')
        layout.addWidget(self.new_text_input)

        self.generate_text_button = QPushButton('Generate New Text', self)
        self.generate_text_button.clicked.connect(self.generate_new_text)
        layout.addWidget(self.generate_text_button)

        self.shortest_path_label = QLabel('Find Shortest Path:', self)
        layout.addWidget(self.shortest_path_label)

        self.shortest_word1_input = QLineEdit(self)
        self.shortest_word1_input.setPlaceholderText('Word 1')
        layout.addWidget(self.shortest_word1_input)

        self.shortest_word2_input = QLineEdit(self)
        self.shortest_word2_input.setPlaceholderText('Word 2')
        layout.addWidget(self.shortest_word2_input)

        self.find_shortest_path_button = QPushButton('Find Shortest Path', self)
        self.find_shortest_path_button.clicked.connect(self.find_shortest_path)
        layout.addWidget(self.find_shortest_path_button)

        self.random_walk_button = QPushButton('Random Walk', self)
        self.random_walk_button.clicked.connect(self.random_walk)
        layout.addWidget(self.random_walk_button)

        self.result_label = QLabel('', self)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文本文件", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            text = read_file(file_name)
            self.text_edit.setPlainText(text)
            self.graph = create_directed_graph(text)
            QMessageBox.information(self, "加载完成", "文本文件已加载并生成图。")

    def draw_graph(self):
        if self.graph:
            draw_graph(self.graph)
        else:
            QMessageBox.warning(self, "错误", "请先加载一个文本文件。")

    def find_bridge_words(self):
        if not self.graph:
            QMessageBox.warning(self, "错误", "请先加载一个文本文件。")
            return
        word1 = self.word1_input.text().lower()
        word2 = self.word2_input.text().lower()
        bridge_words = find_bridge_words(self.graph, word1, word2)

        if bridge_words is None:
            QMessageBox.information(self, "结果", f"No {word1} or {word2} in the graph!")
        elif not bridge_words:
            QMessageBox.information(self, "结果", f"No bridge words from {word1} to {word2}!")
        else:
            QMessageBox.information(self, "结果", f"The bridge words from {word1} to {word2} are: {', '.join(bridge_words)}.")

    def generate_new_text(self):
        if not self.graph:
            QMessageBox.warning(self, "错误", "请先加载一个文本文件。")
            return
        new_text = self.new_text_input.text()
        modified_text = generate_new_text(self.graph, new_text)
        self.result_label.setText(f"生成的新文本为：{modified_text}")

    def find_shortest_path(self):
        if not self.graph:
            QMessageBox.warning(self, "错误", "请先加载一个文本文件。")
            return
        word1 = self.shortest_word1_input.text().lower()
        word2 = self.shortest_word2_input.text().lower()
    
        if word1 != '' and word2 != '':
            length, path = find_shortest_path(self.graph, word1, word2)
        elif word2 == '' and word1 != '':
            while True:
                word2 = random.choice(list(self.graph.nodes))
                length, path = find_shortest_path(self.graph, word1, word2)
                if path != None:
                    break
        if path is None:
            QMessageBox.information(self, "结果", f"No path from {word1} to {word2}!")
        else:
            QMessageBox.information(self, "结果", f"The shortest path from {word1} to {word2} is: {' → '.join(path)} with length {length}.")
            draw_graph(self.graph, path)

    def random_walk(self):
        if not self.graph:
            QMessageBox.warning(self, "错误", "请先加载一个文本文件。")
            return
        walk = random_walk(self.graph)
        walk_text = ' '.join(walk)
        self.result_label.setText(f"随机游走结果：{walk_text}")
        with open("random_walk.txt", 'w', encoding='utf-8') as file:
            file.write(walk_text)
        QMessageBox.information(self, "结果", "随机游走结果已保存到random_walk.txt")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = TextToGraphApp()
    main_win.show()
    sys.exit(app.exec_())
