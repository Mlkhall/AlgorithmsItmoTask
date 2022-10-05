import random
import timeit

import networkx as nx
import numpy as np


def dist(a: tuple[int, int], b: tuple[int, int]) -> float:
    x1, y1 = a
    x2, y2 = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def main(n: int = 100, m: int = 500):
    graph = nx.gnm_random_graph(n, m, seed=10)

    for _, n_brs in graph.adjacency():

        for _, e_attr in n_brs.items():

            e_attr.setdefault('weight', random.randint(1, 100))

    adjacency_matrix = nx.adjacency_matrix(graph)
    adjacency_matrix = adjacency_matrix.todense()

    print('-' * 50)
    print('Adjacency matrix:', adjacency_matrix, sep='\n')
    print('-' * 50)

    d_time = []
    for _ in range(10):
        start_time = timeit.default_timer()
        for i in range(0, 100):
            nx.dijkstra_path(graph, 0, i)

        elapsed = timeit.default_timer() - start_time
        d_time.append(elapsed)

    d_time = np.array(d_time, dtype=np.float16)
    print('Dijkstra time:', d_time.mean())
    print('-' * 50)

    d_time = []
    for _ in range(10):
        start_time = timeit.default_timer()
        for i in range(0, 100):
            nx.bellman_ford_path(graph, 0, i)

        elapsed = timeit.default_timer() - start_time
        d_time.append(elapsed)

    d_time = np.array(d_time, dtype=np.float16)
    print('Bellman-Ford time:', d_time.mean())
    print('-' * 50)

    graph_gg = nx.grid_graph(dim=[10, 10])
    nx.set_edge_attributes(graph_gg, {e: e[1][0] * 2 for e in graph_gg.edges()}, "cost")
    print("A* path:",  nx.astar_path(graph_gg, (0, 0), (2, 8), heuristic=dist, weight="cost"))


if __name__ == "__main__":
    main()