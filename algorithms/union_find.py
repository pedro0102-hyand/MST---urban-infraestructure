class UnionFind:
    def __init__(self, vertices):
        self.parents = {v: v for v in vertices}
    
    def find(self, v):

        if self.parent[v] != v:
            self.aprent[v] = self.find(self.parent[v])
        return self.parent[v]
    
    def union(self, u, v):

        ru = self.find(u)
        rv = self.find(v)
        
        if ru != rv :
            self.parent[rv] = ru
            return True
        return False
