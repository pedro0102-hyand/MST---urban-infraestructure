
# Controle de componentes conexos
# Deteccao de Ciclos
class UnionFind:

    def __init__(self, vertices):

        self.parent = {v: v for v in vertices}

    def find(self, v): #logica de encontrar representante

        if self.parent[v] != v:

            self.parent[v] = self.find(self.parent[v])

        return self.parent[v]

    def union(self, u, v): #logica de conexao de dois conjuntos

        ru = self.find(u)
        rv = self.find(v)

        if ru != rv:

            self.parent[rv] = ru
            return True
        
        return False

