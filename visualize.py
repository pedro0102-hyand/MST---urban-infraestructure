import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import PillowWriter
import os

def create_networkx_graph(graph):
    """Converte o grafo customizado para NetworkX"""
    G = nx.Graph()
    for u, v, weight in graph.edges:
        G.add_edge(u, v, weight=weight)
    return G

def get_layout(G):
    """Gera layout consistente para o grafo"""
    return nx.spring_layout(G, seed=42, k=2, iterations=50)

def draw_graph_state(G, pos, edges_in_mst, current_edge=None, visited_nodes=None, 
                     title="Grafo", step_info=""):
    """Desenha o estado atual do grafo"""
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(12, 8)
    
    # Desenhar todas as arestas em cinza claro
    nx.draw_networkx_edges(G, pos, edge_color='#CCCCCC', width=2, alpha=0.3)
    
    # Desenhar arestas já na MST em verde
    if edges_in_mst:
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_mst, 
                              edge_color='#2ECC71', width=4)
    
    # Destacar aresta sendo considerada em amarelo
    if current_edge:
        nx.draw_networkx_edges(G, pos, edgelist=[current_edge], 
                              edge_color='#F39C12', width=4, style='dashed')
    
    # Desenhar nós
    node_colors = []
    for node in G.nodes():
        if visited_nodes and node in visited_nodes:
            node_colors.append('#3498DB')  # Azul para visitados
        else:
            node_colors.append('#ECF0F1')  # Cinza claro para não visitados
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=1500, edgecolors='#2C3E50', linewidths=3)
    
    # Labels dos nós
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Labels dos pesos nas arestas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9)
    
    # Título e informações
    plt.title(f"{title}\n{step_info}", fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()

def visualize_original_graph(graph, filename="results/grafo_original.png"):
    """Gera imagem do grafo original"""
    os.makedirs("results", exist_ok=True)
    
    G = create_networkx_graph(graph)
    pos = get_layout(G)
    
    plt.figure(figsize=(12, 8))
    draw_graph_state(G, pos, [], title="Grafo Original - Conexões entre Bairros")
    
    # Adicionar legenda
    total_weight = sum(w for _, _, w in graph.edges)
    plt.text(0.02, 0.98, f"Total de arestas: {len(graph.edges)}\nPeso total: {total_weight}", 
             transform=plt.gcf().transFigure, fontsize=11, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Grafo original salvo em: {filename}")

def visualize_prim_gif(graph, start_vertex, filename="results/prim_animation.gif"):
    """Gera GIF animado do algoritmo de Prim"""
    import heapq
    
    os.makedirs("results", exist_ok=True)
    
    G = create_networkx_graph(graph)
    pos = get_layout(G)
    
    # Configurar writer para GIF
    fig = plt.figure(figsize=(12, 8))
    writer = PillowWriter(fps=1)
    
    # Estruturas do algoritmo
    visited = set()
    mst_edges = []
    total_cost = 0
    pq = [(0, start_vertex, None)]
    
    frames = []
    
    # Frame inicial
    frames.append({
        'mst_edges': [],
        'current_edge': None,
        'visited': set(),
        'info': f"Iniciando no vértice: {start_vertex}"
    })
    
    with writer.saving(fig, filename, dpi=100):
        step = 0
        
        while pq:
            cost, u, parent = heapq.heappop(pq)
            
            if u in visited:
                continue
            
            visited.add(u)
            total_cost += cost
            
            current_edge = None
            if parent:
                edge = (parent, u) if (parent, u) in G.edges() else (u, parent)
                mst_edges.append(edge)
                current_edge = edge
                step += 1
                
                # Frame mostrando a aresta sendo adicionada
                draw_graph_state(G, pos, mst_edges[:-1], current_edge, visited,
                               title="Algoritmo de Prim",
                               step_info=f"Passo {step}: Adicionando aresta {parent} → {u} (peso: {cost})\nCusto acumulado: {total_cost}")
                writer.grab_frame()
                
                # Frame com a aresta já na MST
                draw_graph_state(G, pos, mst_edges, None, visited,
                               title="Algoritmo de Prim",
                               step_info=f"Passo {step}: Aresta adicionada à MST\nCusto acumulado: {total_cost}")
                writer.grab_frame()
            
            # Adicionar vizinhos à fila
            for v, weight in graph.adj[u]:
                if v not in visited:
                    heapq.heappush(pq, (weight, v, u))
        
        # Frame final
        draw_graph_state(G, pos, mst_edges, None, visited,
                       title="Algoritmo de Prim - CONCLUÍDO",
                       step_info=f"MST completa com {len(mst_edges)} arestas\nCusto total: {total_cost}")
        writer.grab_frame()
        writer.grab_frame()  # Pausa no final
    
    plt.close()
    print(f"✓ Animação do Prim salva em: {filename}")
    return mst_edges, total_cost

def visualize_kruskal_gif(graph, filename="results/kruskal_animation.gif"):
    """Gera GIF animado do algoritmo de Kruskal"""
    from algorithms.union_find import UnionFind
    
    os.makedirs("results", exist_ok=True)
    
    G = create_networkx_graph(graph)
    pos = get_layout(G)
    
    fig = plt.figure(figsize=(12, 8))
    writer = PillowWriter(fps=1)
    
    uf = UnionFind(graph.vertices())
    edges = sorted(graph.edges, key=lambda x: x[2])
    mst_edges = []
    total_cost = 0
    
    with writer.saving(fig, filename, dpi=100):
        # Frame inicial
        draw_graph_state(G, pos, [], None, set(),
                       title="Algoritmo de Kruskal",
                       step_info="Arestas ordenadas por peso. Iniciando verificação...")
        writer.grab_frame()
        
        step = 0
        for u, v, w in edges:
            step += 1
            edge = (u, v) if (u, v) in G.edges() else (v, u)
            
            # Frame considerando a aresta
            draw_graph_state(G, pos, mst_edges, edge, set(),
                           title="Algoritmo de Kruskal",
                           step_info=f"Passo {step}: Verificando aresta {u} → {v} (peso: {w})")
            writer.grab_frame()
            
            if uf.union(u, v):
                mst_edges.append(edge)
                total_cost += w
                
                # Frame adicionando à MST
                draw_graph_state(G, pos, mst_edges, None, set(),
                               title="Algoritmo de Kruskal",
                               step_info=f"Passo {step}: ✓ Aresta aceita (não forma ciclo)\nCusto acumulado: {total_cost}")
                writer.grab_frame()
            else:
                # Frame rejeitando (formaria ciclo)
                draw_graph_state(G, pos, mst_edges, None, set(),
                               title="Algoritmo de Kruskal",
                               step_info=f"Passo {step}: ✗ Aresta rejeitada (formaria ciclo)\nCusto acumulado: {total_cost}")
                writer.grab_frame()
        
        # Frame final
        draw_graph_state(G, pos, mst_edges, None, set(),
                       title="Algoritmo de Kruskal - CONCLUÍDO",
                       step_info=f"MST completa com {len(mst_edges)} arestas\nCusto total: {total_cost}")
        writer.grab_frame()
        writer.grab_frame()  # Pausa no final
    
    plt.close()
    print(f"✓ Animação do Kruskal salva em: {filename}")
    return mst_edges, total_cost

def generate_all_visualizations(graph, start_vertex=None):
    """Gera todas as visualizações de uma vez"""
    print("\n" + "="*50)
    print("GERANDO VISUALIZAÇÕES")
    print("="*50 + "\n")
    
    # Grafo original
    visualize_original_graph(graph)
    
    # Determinar vértice inicial se não fornecido
    if start_vertex is None:
        start_vertex = next(iter(graph.vertices()))
    
    # Animação Prim
    print("\nGerando animação do Prim...")
    mst_prim, cost_prim = visualize_prim_gif(graph, start_vertex)
    
    # Animação Kruskal
    print("\nGerando animação do Kruskal...")
    mst_kruskal, cost_kruskal = visualize_kruskal_gif(graph)
    
    print("\n" + "="*50)
    print("VISUALIZAÇÕES CONCLUÍDAS")
    print("="*50)
    print(f"\nArquivos salvos em: ./results/")
    print(f"  - grafo_original.png")
    print(f"  - prim_animation.gif")
    print(f"  - kruskal_animation.gif")
    print(f"\nCusto MST (Prim): {cost_prim}")
    print(f"Custo MST (Kruskal): {cost_kruskal}")
    print()