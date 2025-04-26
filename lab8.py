from collections import deque
import random

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0] * vertices for _ in range(vertices)]

    # Поиск в ширину для поиска пути с положительным потоком
    def bfs(self, s, t, parent):
        visited = [False] * self.V
        queue = deque()

        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.popleft()

            for v, capacity in enumerate(self.graph[u]):
                if not visited[v] and capacity > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u

        return visited[t]

    # Реализация алгоритма Эдмондса-Карпа (модификация Форда-Фалкерсона)
    def edmonds_karp(self, source, sink):
        parent = [-1] * self.V
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow

    # Для нахождения минимального разреза после расчета потока
    def dfs(self, s, visited):
        visited[s] = True
        for i, capacity in enumerate(self.graph[s]):
            if capacity > 0 and not visited[i]:
                self.dfs(i, visited)

    def min_cut(self, source):
        visited = [False] * self.V
        self.dfs(source, visited)
        cut_edges = []
        for i in range(self.V):
            for j in range(self.V):
                if visited[i] and not visited[j] and original_graph[i][j] > 0:
                    cut_edges.append((i, j))
        return cut_edges

def build_correct_graph():
    g = Graph(11)  # 11 вершин: 0..10
    g.graph = [
        [0, 50, 30, 15, 0, 0, 0, 0, 0, 0, 0],  # 0 (S)
        [0, 0, 50, 0, 25, 0, 0, 0, 0, 0, 0],   # 1
        [0, 0, 0, 0, 45, 10, 0, 15, 0, 0, 0],  # 2
        [0, 0, 15, 0, 0, 10, 0, 0, 20, 0, 0],  # 3
        [0, 0, 0, 0, 0, 0, 90, 10, 0, 0, 0],   # 4
        [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0],    # 5
        [0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 10],   # 6
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 80],   # 7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],    # 8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],    # 9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     # 10 (T)
    ]
    return g

def run_flow(g, source, sink):
    global original_graph
    original_graph = [row[:] for row in g.graph]  # Сохраняем копию для поиска разреза
    max_flow = g.edmonds_karp(source, sink)
    print(f"Максимальный поток: {max_flow}")

    cut_edges = g.min_cut(source)
    print("Минимальный разрез:")
    for u, v in cut_edges:
        print(f"{u} -> {v}")

def randomize_capacities(g, lower=100, upper=1000):
    for i in range(g.V):
        for j in range(g.V):
            if original_graph[i][j] > 0:
                g.graph[i][j] = random.randint(lower, upper)

if __name__ == "__main__":
    print("Рассчитываем по исходной сети:")
    g = build_correct_graph()
    run_flow(g, 0, 10)

    print("\nРассчитываем по сети со случайными пропускными способностями:")
    g_random = build_correct_graph()
    randomize_capacities(g_random)
    run_flow(g_random, 0, 10)
