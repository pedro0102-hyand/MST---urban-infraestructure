class Graph:
    def __init__(self):
        
        self.adj = {} # lista de adjascencias
        self.edges = [] 
    
    # Registra as conexoes e atualiza as estruturas de dados
    def add_edge(self, u, v, weight):

        self.edges.append((u,v,weight))

        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))
    
    def vertices(self):
        return self.adj.keys()