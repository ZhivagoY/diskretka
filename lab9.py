import matplotlib.pyplot as plt
import networkx as nx

def ford_fulkerson_matching(edges):
    # Создаем граф
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # Разбиваем вершины на две доли (простая эвристика)
    left = set()
    right = set()
    for u, v in edges:
        if u not in right:
            left.add(u)
            right.add(v)
        elif v not in right:
            left.add(v)
            right.add(u)
    
    # Создаем сеть для алгоритма Форда-Фалкерсона
    flow_graph = nx.DiGraph()
    flow_graph.add_node('source')
    flow_graph.add_node('sink')
    
    for node in left:
        flow_graph.add_edge('source', node, capacity=1)
    for node in right:
        flow_graph.add_edge(node, 'sink', capacity=1)
    for u, v in edges:
        if u in left and v in right:
            flow_graph.add_edge(u, v, capacity=1)
        elif v in left and u in right:
            flow_graph.add_edge(v, u, capacity=1)
    
    # Вычисляем максимальный поток
    flow_value, flow_dict = nx.maximum_flow(flow_graph, 'source', 'sink')
    
    # Восстанавливаем паросочетание
    matching = []
    for u in left:
        for v in flow_graph.successors(u):
            if v != 'sink' and flow_dict[u][v] > 0:
                matching.append((u, v))
    
    return matching
    
def kuhn_matching(edges):
    # Создаем граф
    G = {}
    for u, v in edges:
        if u not in G:
            G[u] = []
        if v not in G:
            G[v] = []
        G[u].append(v)
        G[v].append(u)
    
    # Разбиваем вершины на две доли (простая эвристика)
    left = set()
    right = set()
    for u, v in edges:
        if u not in right:
            left.add(u)
            right.add(v)
        elif v not in right:
            left.add(v)
            right.add(u)
    
    # Реализация алгоритма Куна
    match_to = {}
    result = 0
    
    def bpm(u, seen):
        for v in G[u]:
            if v not in seen:
                seen.add(v)
                if v not in match_to or bpm(match_to[v], seen):
                    match_to[v] = u
                    return True
        return False
    
    for u in left:
        if bpm(u, set()):
            result += 1
    
    # Формируем список пар
    matching = [(match_to[v], v) for v in match_to]
    return matching

def visualize_graph(edges, matching_edges=None, title="Graph"):
    G = nx.Graph()
    G.add_edges_from(edges)
    
    pos = nx.spring_layout(G)
    
    # Рисуем все ребра серым цветом
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1)
    
    # Если задано паросочетание, рисуем его красным
    if matching_edges:
        matching_graph = nx.Graph()
        matching_graph.add_edges_from(matching_edges)
        nx.draw_networkx_edges(matching_graph, pos, edge_color='red', width=2)
    
    # Рисуем вершины
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos)
    
    plt.title(title)
    plt.axis('off')
    plt.show()

# Пример использования
edges = [(7, 10), (7, 14), (9, 14), (2, 11), (7, 8), (2, 6), (3, 6),
         (9, 10), (7, 12), (5, 6), (3, 9), (2, 7), (5, 9), (6, 10),
         (2, 9), (3, 11), (11, 15), (6, 13), (6, 16), (9, 15), (4, 6),
         (6, 12), (5, 7), (11, 13), (6, 15), (7, 15), (6, 8), (8, 9),
         (7, 13), (9, 16), (11, 14), (4, 11), (5, 11), (4, 7), (3, 7)]

# Удаляем несколько ребер для получения двудольного графа
bipartite_edges = [e for e in edges if e not in {(3,7), (5,7), (7,15)}]

# Находим паросочетание
matching_ff = ford_fulkerson_matching(bipartite_edges)
matching_kuhn = kuhn_matching(bipartite_edges)

# Визуализируем
visualize_graph(bipartite_edges, matching_ff, "Ford-Fulkerson Matching")
visualize_graph(bipartite_edges, matching_kuhn, "Kuhn's Matching")