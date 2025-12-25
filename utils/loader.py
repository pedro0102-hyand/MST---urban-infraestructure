import json
from graph.graph import Graph


def load_graph(path):
    """
    Carrega um grafo a partir de um arquivo JSON.
    Formato esperado:
    [
        ["A", "B", 4],
        ["B", "C", 2],
        ...
    ]
    """
    graph = Graph()

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for u, v, weight in data:
        graph.add_edge(u, v, weight)

    return graph
