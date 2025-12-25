import time

def compare(graph):
    
    from algorithms.prim import prim
    from algorithms.kruskal import kruskal

    start = next(iter(graph.vertices()))

    t1 = time.time()
    _, cost_prim = prim(graph, start)
    t2 = time.time()

    _, cost_kruskal = kruskal(graph)
    t3 = time.time()

    return {
        "Prim": {"cost": cost_prim, "time": t2 - t1},
        "Kruskal": {"cost": cost_kruskal, "time": t3 - t2}
    }
