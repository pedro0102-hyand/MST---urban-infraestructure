from algorithms.union_find import UnionFind

def kruskal(graph):

    mst = []
    total_cost = 0

    uf = UnionFind(graph.vertices())
    edges = sorted(graph.edges, key = lambda x : x[2])

    for u, v , w in edges:
        if uf.union(u, v):
            mst.append((u,v,w))
            total_cost += w
    
    return mst, total_cost