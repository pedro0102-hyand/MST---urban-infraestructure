import heapq

def prim(graph, start):

    visited = set()
    mst = []
    total_cost = 0

    pq = [(0, start, None)]

    while pq:
        cost, u, parent = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)
        total_cost = total_cost + cost

        if parent:
            mst.append((parent,u,cost))

        for v, weight in graph.adj[u]:
            if v not in visited :
                heapq.heappush(pq, (weight, v, u))
    
    return mst, total_cost