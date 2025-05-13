import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import random

class FordFulkerson:
    def __init__(self, graph):
        # Инициализация графа и множества посещённых вершин
        self.graph = graph  # Граф представлен в виде словаря
        self.visited = set()  # Множество для отслеживания посещённых вершин

    def ford_fulkerson(self, source, sink):
        max_flow = 0

        while True:
            # Поиск пути от source к sink с помощью DFS
            path = self._dfs(source, sink, [])
            if not path:
                break

            # Определение минимальной ёмкости по найденному пути
            min_capacity = float("inf")
            for u, v in path:
                min_capacity = min(min_capacity, self.graph[u][v])  # Находим минимальную ёмкость

            # Обновление пропускных способностей по найденному пути
            for u, v in path:
                self.graph[u][v] -= min_capacity  # Уменьшаем ёмкость прямого ребра
                self.graph[v][u] += min_capacity  # Увеличиваем ёмкость обратного ребра

            max_flow += min_capacity  # Увеличиваем общий максимальный поток

        return max_flow

    def _dfs(self, node, sink, path):
        # Метод для поиска пути с помощью DFS
        if node == sink:
            return path  # Если достигли sink, возвращаем текущий путь
        self.visited.add(node)  # Добавляем текущую вершину в множество посещённых
        for next_node, capacity in self.graph[node].items():
            # Перебираем соседние вершины
            if next_node not in self.visited and capacity > 0:  # Если вершина не посещена и ёмкость положительна
                new_path = path + [(node, next_node)]  # Добавляем текущее ребро в путь
                result = self._dfs(next_node, sink, new_path)  # Рекурсивный вызов для следующей вершины
                if result:
                    return result
        return None

    def min_cut(self, source):
        # Метод для нахождения минимального разреза
        self.visited.add(source)  # Добавляем начальную вершину в множество посещённых
        reachable_nodes = set()  # Множество для хранения достижимых вершин

        stack = [source]  # Стек для обхода графа
        while stack:
            node = stack.pop()  # Извлекаем вершину из стека
            reachable_nodes.add(node)  # Добавляем её в множество достижимых
            for next_node, capacity in self.graph[node].items():
                # Перебираем соседние вершины
                if next_node not in self.visited and capacity > 0:
                    stack.append(next_node)  # Добавляем в стек для дальнейшего обхода
                    self.visited.add(next_node)  # Помечаем как посещённую

        min_cut = []
        for u in reachable_nodes:
            for v, capacity in self.graph[u].items():
                if v not in reachable_nodes:
                    min_cut.append((u, v))  # Если v недостижима, добавляем ребро в минимальный разрез

        return min_cut  # Возвращаем найденный минимальный разрез

def visualize_graph(edges):
    G = nx.DiGraph()
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=500, font_size=12, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): str(d["capacity"]) for u, v, d in G.edges(data=True)})
    plt.title("Граф сети")
    plt.show()

def find_max_flow_min_cut(edges):
    G = nx.DiGraph()

    for edge in edges:
        G.add_edge(edge[0], edge[1], capacity=edge[2])

    source = 'S'  # Заменяем на буквы
    sink = 'T'    # Заменяем на буквы
    flow_value, flow_dict = nx.maximum_flow(G, source, sink)
    min_cut = nx.minimum_cut(G, source, sink)

    return flow_value, min_cut

# Список рёбер сети
edges = [['S', '1', 50], ['S', '2', 30], ['S', '3', 15],
         ['1', '4', 25], 
         ['2', '1', 50], ['2', '4', 45], ['2', '7', 15], 
         ['3', '2', 15], ['3', '5', 10], ['3', '8', 20],
         ['4', '6', 90], ['4', '7', 10], 
         ['5', '2', 10],
         ['6', 'T', 10], 
         ['7', '2', 15], ['7', '5', 60], ['7', '6', 10], ['7', '9', 10], ['7', 'T', 80],
         ['8', '7', 20], ['8', '9', 10], 
         ['9', 'T', 10]]

# Находим максимальный поток и минимальный разрез
max_flow, min_cut = find_max_flow_min_cut(edges)

print("Максимальный поток:", max_flow)
print("Минимальный разрез:", min_cut)

# Визуализируем граф
visualize_graph(edges)

# построим граф с другими весами
edges2 = []
for i in range(len(edges)):
    cur_edge = edges[i]
    cur_edge[2] = random.randint(100, 1000)
    edges2.append(cur_edge)

max_flow2, min_cut2 = find_max_flow_min_cut(edges2)

print("Максимальный поток:", max_flow2)
print("Минимальный разрез:", min_cut2)
graph2 = defaultdict(dict)
for u, v, capacity in edges2:
    graph2[u][v] = capacity
    graph2[v][u] = 0  # Обратные рёбра для обратного потока

visualize_graph(edges2)