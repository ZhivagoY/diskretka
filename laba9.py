import matplotlib.pyplot as plt
from collections import defaultdict, deque
import networkx as nx

edges = [(7, 10), (7, 14), (9, 14), (2, 11), (7, 8), (2, 6), (3, 6),
         (9, 10), (7, 12), (5, 6), (3, 9), (2, 7), (5, 9), (6, 10),
         (2, 9), (3, 11), (11, 15), (6, 13), (6, 16), (9, 15), (4, 6),
         (6, 12), (5, 7), (11, 13), (6, 15), (7, 15), (6, 8), (8, 9),
         (7, 13), (9, 16), (11, 14), (4, 11), (5, 11), (4, 7), (3, 7)]

def is_bipartite(edges):
    graph = {}
    for edge in edges:
        u, v = edge
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    if not graph:
        print("Граф пустой.")
        return False, None, None

    colors = {}
    start_node = next(iter(graph))
    queue = deque([start_node])
    colors[start_node] = 0

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in colors:
                colors[neighbor] = 1 - colors[current]
                queue.append(neighbor)
            elif colors[neighbor] == colors[current]:
                print("Граф не двудольный.")
                return False, None, None

    # Разделение на доли
    part1 = [node for node, color in colors.items() if color == 0]
    part2 = [node for node, color in colors.items() if color == 1]

    return True, part1, part2

def build_flow_network(graph, part1, part2):
    """
    Строит сеть потока на основе двудольного графа.
    """
    flow_network = defaultdict(dict)
    source = "source"
    sink = "sink"

    # Добавляем вершины источника и стока
    all_nodes = list(graph.keys())  # Все узлы исходного графа

    # Соединяем источник со всеми вершинами первой доли
    for node in part1:
        flow_network[source][node] = 1

    # Соединяем все вершины второй доли со стоком
    for node in part2:
        flow_network[node][sink] = 1

    # Добавляем ребра исходного графа с пропускной способностью 1
    for u in graph:
        for v in graph[u]:
            if u in part1 and v in part2:
                flow_network[u][v] = 1  # Прямое ребро
            elif v in part1 and u in part2:
                flow_network[v][u] = 1  # Прямое ребро, словарь смежности

    # Добавляем обратные ребра с пропускной способностью 0
    for u in all_nodes + [source, sink]:
      for v in all_nodes + [source, sink]:
        if u not in flow_network:
          flow_network[u] = {}
        if v not in flow_network[u]:
          flow_network[u][v] = 0 #Инициализация остаточной пропускной способности

    return flow_network, source, sink

def bfs(graph, source, sink, parent):
    """
    Поиск в ширину для нахождения увеличивающего пути.
    """
    visited = {node: False for node in graph}
    queue = deque([source])
    visited[source] = True
    parent[source] = None  # Важно: инициализация parent[source]

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if not visited[v] and graph[u][v] > 0:  # Проверяем остаточную пропускную способность
                queue.append(v)
                visited[v] = True
                parent[v] = u

    return visited[sink]  # True, если есть путь до стока, False иначе

def ford_fulkerson(graph, source, sink):
    """
    Алгоритм Форда-Фалкерсона для нахождения максимального потока.
    """
    max_flow = 0
    parent = {}  # Словарь для хранения родительских узлов на пути

    while bfs(graph, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow

        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow  # Уменьшаем пропускную способность прямого ребра
            graph[v][u] += path_flow  # Увеличиваем пропускную способность обратного ребра
            v = parent[v]
    return max_flow

def extract_matching(flow_network, part1, part2, source, sink):
    """
    Извлекает ребра паросочетания из сети потока.
    """
    matching = []
    for u in part1:
        for v in part2:
            if flow_network[u][v] == 0 and flow_network[v][u] == 1:
                matching.append((u, v))
    return matching

class GraphK:
    def __init__(self, edges):
        self.graph = {}
        self.visited = set()
        self.matched = {}  # Словарь для паросочетаний
        self.construct_graph(edges)

    def construct_graph(self, edges):
        for u, v in edges:
            if u not in self.graph:
                self.graph[u] = []
            if v not in self.graph:
                self.graph[v] = []
            self.graph[u].append(v)
            self.graph[v].append(u) # Добавляем обратное ребро для неориентированного графа
            self.matched[u] = None
            self.matched[v] = None

    def dfs(self, u):
        """
        Рекурсивно ищет увеличивающий путь в графе с помощью поиска в глубину (DFS).
        :param u: Текущая вершина.
        :return: True, если увеличивающий путь найден, иначе False.
        """
        if u in self.visited:
            return False
        self.visited.add(u)
        if u not in self.graph:
            return False # Если у вершины нет соседей

        for v in self.graph[u]:  # Перебираем всех соседей вершины u
            if self.matched[v] is None or (v in self.matched and self.dfs(self.matched[v])):
                # Если сосед v не сопоставлен или нашли увеличивающий путь от вершины, с которой сопоставлен v
                self.matched[u] = v  # Сопоставляем вершину u с вершиной v
                self.matched[v] = u  # Сопоставляем вершину v с вершиной u
                return True  # Возвращаем True, так как увеличивающий путь найден
        return False  # Если увеличивающий путь не найден, возвращаем False

    def max_matching(self):
        """
        Находит максимальное паросочетание в графе.
        :return: Количество рёбер в максимальном паросочетании и список этих рёбер.
        """
        matchings = 0  # Инициализируем количество рёбер в паросочетании
        for u in self.graph:  # Перебираем все вершины графа
            if self.matched[u] is None:  # Если вершина не сопоставлена
                self.visited = set()  # Очищаем множество посещённых вершин перед каждым поиском пути (важно для алгоритма Куна)
                if self.dfs(u):  # Пытаемся найти увеличивающий путь, начиная с этой вершины
                    matchings += 1  # Если увеличивающий путь найден, увеличиваем количество рёбер в паросочетании
        matching_edges = [(u, v) for u, v in self.matched.items() if v is not None and u < v ]  # Формируем список рёбер паросочетания, убираем дубликаты
        return matchings, matching_edges  # Возвращаем количество рёбер и список рёбер паросочетания


def visualize_graph(edges, matching_edges_ford_fulkerson=None, matching_edges_kuhn=None):
    graph = nx.Graph(edges)
    pos = nx.spring_layout(graph)  # Layout for graph visualization

    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)

    if matching_edges_ford_fulkerson:
        nx.draw_networkx_edges(graph, pos, edgelist=matching_edges_ford_fulkerson, edge_color='red', width=2)
    if matching_edges_kuhn:
        nx.draw_networkx_edges(graph, pos, edgelist=matching_edges_kuhn, edge_color='green', width=2)

    plt.show()

# 1. Проверка двудольности
is_bipartite_result, part1, part2 = is_bipartite(edges)

if is_bipartite_result:
    print("Граф двудольный.")
    print("Первая доля:", part1)
    print("Вторая доля:", part2)

    # Создание представления графа в виде словаря смежности
    graph_dict = defaultdict(list)
    for u, v in edges:
        graph_dict[u].append(v)
        graph_dict[v].append(u)

    # 2.2-2.3. Создание сети потока и модернизация
    flow_network, source, sink = build_flow_network(graph_dict, part1, part2)

    # 2.4. Поиск максимального потока
    max_flow = ford_fulkerson(flow_network, source, sink)
    print("\nАлгоритм Форда-Фалкерсона:")
    print("Максимальный поток:", max_flow)

    # 2.5. Извлечение ребер паросочетания
    matching_edges_ford_fulkerson = extract_matching(flow_network, part1, part2, source, sink)
    print("Ребра паросочетания:", matching_edges_ford_fulkerson)

    # 2.6. Подсчет количества ребер
    num_matches_ford_fulkerson = len(matching_edges_ford_fulkerson)
    print("Количество ребер в паросочетании:", num_matches_ford_fulkerson)

    # Алгоритм Куна
    print("\nАлгоритм Куна:")
    graph_kuhn = GraphK(edges)
    num_matches_kuhn, matching_edges_kuhn = graph_kuhn.max_matching()

    print("Число максимального паросочетания:", num_matches_kuhn)
    print("Рёбра, входящие в максимальное паросочетание:", matching_edges_kuhn)

    # Визуализация графа с обоими паросочетаниями
    visualize_graph(edges, matching_edges_ford_fulkerson, matching_edges_kuhn)


else:
    print("Граф не двудольный. Алгоритм не может быть применен.")

print("\nДвудольный граф или биграф – это граф, множество вершин которого можно разбить на две части таким образом, что каждое ребро графа соединяет какую-то вершину из одной части с какой-то вершиной другой части, то есть не существует ребра, соединяющего две вершины из одной и той же части.\n",
      "\nПаросочетание в графе — это множество рёбер, попарно не имеющих общих вершин.\n",
      "\nСвойства алгоритмов:\n", "1. Эвристический алгоритм:\n",
      "•  Простота реализации: Его можно легко реализовать, используя циклы и структуры данных для отслеживания вершин и ребер.\n",
      "•  Скорость: Быстрее, чем алгоритмы Куна и Форда-Фалкерсона на больших графах, но с риском получения неоптимального решения.\n",
      "•  Негарантированный максимум: Например, если алгоритм сначала выберет ребро, соединяющее вершину с малой степенью, но это заблокирует выбор других ребер, которые могли бы привести к большему паросочетанию.\n",
      "\n2. Алгоритм Куна:\n", "•  Гарантированный максимум: Всегда находит максимальное паросочетание.\n",
      "•  Использование DFS: В коде это реализовано рекурсивной функцией dfs.\n",
      "•  Сложность: Может быть медленнее эвристического алгоритма на больших графах, но все еще достаточно эффективен.\n",
      "\n3. Алгоритм Форда-Фалкерсона:\n", "•  Гарантированный максимум: Всегда находит максимальное паросочетание.\n",
      "•  Сеть потоков: Требует построения сети потока на основе двудольного графа.\n",
      "•  BFS для поиска путей: Использует BFS (bfs функция) для поиска увеличивающих…")