class Edge :
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight
    
    def __lt__(self, other):
        return self.weight < other.weight