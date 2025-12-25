from algorithms.union_find import UnionFind #verificar se vertices já estao conectados

def kruskal(graph):

    mst = []
    total_cost = 0

    uf = UnionFind(graph.vertices()) #retornar todos os vértices do grafo
    edges = sorted(graph.edges, key = lambda x : x[2]) #ordenacao das arestas por peso

    for u, v , w in edges:

        #verificar se u e v estao no mesmo conjunto
        #se estiverem no mesmo conjunto, criaria ciclos
        #se nao estiveres podemos adicionar na lista e considerar sua aresta

        if uf.union(u, v): 
            mst.append((u,v,w))
            total_cost += w
    
    return mst, total_cost