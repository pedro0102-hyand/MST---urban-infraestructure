from collections import deque, defaultdict

class MSTAnalyzer:
    """Classe para análise de métricas da Árvore Geradora Mínima"""
    
    def __init__(self, mst_edges):
        """
        Inicializa o analisador com as arestas da MST
        
        Args:
            mst_edges: Lista de tuplas (u, v, weight) representando a MST
        """
        self.mst_edges = mst_edges
        self.adj = self._build_adjacency_list()
        self.vertices = list(self.adj.keys())
    
    def _build_adjacency_list(self):
        """Constrói lista de adjacências a partir das arestas da MST"""
        adj = defaultdict(list)
        for u, v, weight in self.mst_edges:
            adj[u].append((v, weight))
            adj[v].append((u, weight))
        return adj
    
    def _bfs_distances(self, start):
        """
        BFS para calcular distâncias de um vértice para todos os outros
        
        Returns:
            dict: {vertice: distancia_total} do vértice inicial
        """
        distances = {start: 0}
        queue = deque([start])
        visited = {start}
        
        while queue:
            u = queue.popleft()
            
            for v, weight in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    distances[v] = distances[u] + weight
                    queue.append(v)
        
        return distances
    
    def calculate_diameter(self):
        """
        Calcula o diâmetro da MST (maior distância entre quaisquer dois vértices)
        
        Returns:
            dict: {
                'diameter': valor do diâmetro,
                'path_vertices': (u, v) vértices das extremidades,
                'distance': distância entre eles
            }
        """
        max_distance = 0
        diameter_vertices = None
        
        # Para cada vértice, calcular distâncias para todos os outros
        for vertex in self.vertices:
            distances = self._bfs_distances(vertex)
            
            # Encontrar a maior distância a partir deste vértice
            for target, dist in distances.items():
                if dist > max_distance:
                    max_distance = dist
                    diameter_vertices = (vertex, target)
        
        return {
            'diameter': max_distance,
            'path_vertices': diameter_vertices,
            'distance': max_distance
        }
    
    def calculate_center_and_radius(self):
        """
        Calcula o centro e o raio da MST
        
        Centro: vértice que minimiza a distância máxima para qualquer outro vértice
        Raio: a menor das distâncias máximas (excentricidade do centro)
        
        Returns:
            dict: {
                'center': vértice central,
                'radius': raio da MST,
                'eccentricity': distância máxima do centro,
                'all_eccentricities': {vertice: excentricidade}
            }
        """
        eccentricities = {}
        
        # Calcular excentricidade de cada vértice
        # (maior distância daquele vértice para qualquer outro)
        for vertex in self.vertices:
            distances = self._bfs_distances(vertex)
            eccentricity = max(distances.values()) if distances else 0
            eccentricities[vertex] = eccentricity
        
        # Centro é o vértice com menor excentricidade
        center = min(eccentricities, key=eccentricities.get)
        radius = eccentricities[center]
        
        return {
            'center': center,
            'radius': radius,
            'eccentricity': radius,
            'all_eccentricities': eccentricities
        }
    
    def analyze_balance(self):
        """
        Analisa o balanceamento da MST
        
        Verifica:
        - Comprimento dos "braços" (caminhos mais longos)
        - Distribuição de pesos
        - Vértices folha vs internos
        
        Returns:
            dict: {
                'leaf_nodes': lista de vértices folha,
                'leaf_count': número de folhas,
                'internal_count': número de vértices internos,
                'longest_branch': {
                    'from': vértice inicial,
                    'to': vértice final,
                    'length': comprimento do braço,
                    'path': caminho completo
                },
                'average_degree': grau médio dos vértices,
                'degree_distribution': {vertice: grau},
                'balance_score': score de balanceamento (0-1, quanto maior mais balanceado)
            }
        """
        # Identificar vértices folha (grau 1)
        degrees = {v: len(neighbors) for v, neighbors in self.adj.items()}
        leaf_nodes = [v for v, deg in degrees.items() if deg == 1]
        internal_nodes = [v for v, deg in degrees.items() if deg > 1]
        
        # Encontrar o braço mais longo
        longest_branch = self._find_longest_branch()
        
        # Calcular grau médio
        avg_degree = sum(degrees.values()) / len(degrees) if degrees else 0
        
        # Score de balanceamento baseado na variância dos graus
        # e na razão entre folhas e vértices internos
        degree_variance = self._calculate_variance(list(degrees.values()))
        
        # Normalizar score (quanto menor a variância, mais balanceado)
        # Score entre 0 e 1
        max_possible_variance = (len(self.vertices) - 1) ** 2
        balance_score = 1 - (degree_variance / max_possible_variance) if max_possible_variance > 0 else 1
        
        return {
            'leaf_nodes': leaf_nodes,
            'leaf_count': len(leaf_nodes),
            'internal_count': len(internal_nodes),
            'longest_branch': longest_branch,
            'average_degree': round(avg_degree, 2),
            'degree_distribution': degrees,
            'balance_score': round(balance_score, 3)
        }
    
    def _find_longest_branch(self):
        """Encontra o braço (caminho simples) mais longo na MST"""
        max_length = 0
        longest_path = None
        start_vertex = None
        end_vertex = None
        
        # Para cada vértice, fazer DFS e encontrar o caminho mais longo
        for vertex in self.vertices:
            result = self._dfs_longest_path(vertex)
            if result['length'] > max_length:
                max_length = result['length']
                longest_path = result['path']
                start_vertex = vertex
                end_vertex = result['end']
        
        return {
            'from': start_vertex,
            'to': end_vertex,
            'length': max_length,
            'path': longest_path
        }
    
    def _dfs_longest_path(self, start):
        """DFS para encontrar o caminho mais longo a partir de um vértice"""
        max_length = 0
        longest_path = [start]
        end_vertex = start
        
        def dfs(v, visited, current_length, path):
            nonlocal max_length, longest_path, end_vertex
            
            if current_length > max_length:
                max_length = current_length
                longest_path = path.copy()
                end_vertex = v
            
            for neighbor, weight in self.adj[v]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, visited, current_length + weight, path)
                    path.pop()
                    visited.remove(neighbor)
        
        dfs(start, {start}, 0, [start])
        
        return {
            'length': max_length,
            'path': longest_path,
            'end': end_vertex
        }
    
    def _calculate_variance(self, values):
        """Calcula a variância de uma lista de valores"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def get_full_analysis(self):
        """
        Retorna análise completa da MST
        
        Returns:
            dict: Todas as métricas calculadas
        """
        diameter_info = self.calculate_diameter()
        center_info = self.calculate_center_and_radius()
        balance_info = self.analyze_balance()
        
        return {
            'diameter': diameter_info,
            'center_and_radius': center_info,
            'balance': balance_info,
            'summary': {
                'total_vertices': len(self.vertices),
                'total_edges': len(self.mst_edges),
                'total_weight': sum(w for _, _, w in self.mst_edges)
            }
        }
    
    def print_analysis(self):
        """Imprime análise formatada da MST"""
        analysis = self.get_full_analysis()
        
        print("\n" + "="*70)
        print("ANÁLISE DETALHADA DA MST")
        print("="*70)
        
        # Informações gerais
        print("\n📊 INFORMAÇÕES GERAIS")
        print("-" * 70)
        print(f"Total de vértices: {analysis['summary']['total_vertices']}")
        print(f"Total de arestas: {analysis['summary']['total_edges']}")
        print(f"Peso total da MST: {analysis['summary']['total_weight']}")
        
        # Diâmetro
        print("\n📏 DIÂMETRO DA MST")
        print("-" * 70)
        diam = analysis['diameter']
        print(f"Diâmetro: {diam['diameter']}")
        print(f"Caminho mais longo: {diam['path_vertices'][0]} ↔ {diam['path_vertices'][1]}")
        print(f"Distância: {diam['distance']}")
        
        # Centro e Raio
        print("\n🎯 CENTRO E RAIO")
        print("-" * 70)
        center = analysis['center_and_radius']
        print(f"Centro da MST: {center['center']}")
        print(f"Raio: {center['radius']}")
        print(f"Excentricidade do centro: {center['eccentricity']}")
        print("\nExcentricidades de todos os vértices:")
        for v, ecc in sorted(center['all_eccentricities'].items(), 
                            key=lambda x: x[1]):
            print(f"  {v}: {ecc}")
        
        # Balanceamento
        print("\n⚖️  ANÁLISE DE BALANCEAMENTO")
        print("-" * 70)
        balance = analysis['balance']
        print(f"Score de balanceamento: {balance['balance_score']:.3f} (0-1, maior = mais balanceado)")
        print(f"Grau médio dos vértices: {balance['average_degree']}")
        print(f"Vértices folha: {balance['leaf_count']}")
        print(f"Vértices internos: {balance['internal_count']}")
        
        print("\nDistribuição de graus:")
        for v, deg in sorted(balance['degree_distribution'].items(), 
                            key=lambda x: x[1], reverse=True):
            node_type = "🍃 folha" if deg == 1 else "🔗 interno"
            print(f"  {v}: grau {deg} ({node_type})")
        
        print("\nBraço mais longo:")
        branch = balance['longest_branch']
        print(f"  De {branch['from']} até {branch['to']}")
        print(f"  Comprimento: {branch['length']}")
        print(f"  Caminho: {' → '.join(branch['path'])}")
        
        # Recomendações
        print("\n💡 RECOMENDAÇÕES")
        print("-" * 70)
        
        if balance['balance_score'] < 0.5:
            print("⚠️  A MST está desbalanceada. Considere:")
            print("   - Verificar se há conexões alternativas mais equilibradas")
            print("   - Analisar se os 'braços longos' podem ser encurtados")
        else:
            print("✅ A MST está bem balanceada!")
        
        print(f"\n📍 Melhor localização para ponto central: {center['center']}")
        print(f"   (Minimiza a distância máxima para qualquer outro bairro)")
        
        if diam['diameter'] > 2 * center['radius']:
            print("\n⚠️  O diâmetro é muito maior que o raio.")
            print("   Isso indica que a MST é 'alongada' em uma direção.")
        
        print("\n" + "="*70 + "\n")