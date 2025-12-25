"""
Script para testar as métricas da MST com diferentes grafos
"""
from utils.loader import load_graph
from algorithms.prim import prim
from algorithms.kruskal import kruskal
from analysis.mst_metrics import MSTAnalyzer

def test_with_different_graphs():
    """Testa as métricas com diferentes arquivos de grafo"""
    
    graphs_to_test = [
        ("data/bairros.json", "Grafo dos Bairros"),
        ("data/bigger.json", "Grafo Maior")
    ]
    
    for filepath, name in graphs_to_test:
        try:
            print("\n" + "🔷" * 40)
            print(f"TESTANDO: {name}")
            print("🔷" * 40)
            
            # Carregar grafo
            graph = load_graph(filepath)
            print(f"\n✓ Grafo carregado: {len(graph.vertices())} vértices, {len(graph.edges)} arestas")
            
            # Executar Prim
            start = next(iter(graph.vertices()))
            mst_prim, cost_prim = prim(graph, start)
            print(f"✓ MST (Prim) calculada: custo = {cost_prim}")
            
            # Executar Kruskal
            mst_kruskal, cost_kruskal = kruskal(graph)
            print(f"✓ MST (Kruskal) calculada: custo = {cost_kruskal}")
            
            # Verificar se ambos têm o mesmo custo
            if cost_prim == cost_kruskal:
                print(f"✅ Ambos algoritmos encontraram o mesmo custo!")
            
            # Analisar MST com Prim
            print(f"\n{'='*80}")
            print(f"ANÁLISE USANDO MST DO PRIM")
            print(f"{'='*80}")
            analyzer = MSTAnalyzer(mst_prim)
            analyzer.print_analysis()
            
        except FileNotFoundError:
            print(f"⚠️  Arquivo {filepath} não encontrado. Pulando...")
        except Exception as e:
            print(f"❌ Erro ao processar {name}: {e}")

def test_individual_metrics():
    """Testa cada métrica individualmente"""
    print("\n" + "🧪" * 40)
    print("TESTE INDIVIDUAL DE MÉTRICAS")
    print("🧪" * 40)
    
    # Criar um grafo simples para teste
    mst_test = [
        ("A", "B", 1),
        ("B", "C", 2),
        ("C", "D", 1),
        ("B", "E", 3)
    ]
    
    analyzer = MSTAnalyzer(mst_test)
    
    print("\nMST de teste:")
    for u, v, w in mst_test:
        print(f"  {u} - {v} (peso: {w})")
    
    # Testar diâmetro
    print("\n1️⃣  Testando cálculo de diâmetro...")
    diameter = analyzer.calculate_diameter()
    print(f"   Diâmetro: {diameter['diameter']}")
    print(f"   Entre: {diameter['path_vertices']}")
    
    # Testar centro e raio
    print("\n2️⃣  Testando cálculo de centro e raio...")
    center = analyzer.calculate_center_and_radius()
    print(f"   Centro: {center['center']}")
    print(f"   Raio: {center['radius']}")
    
    # Testar balanceamento
    print("\n3️⃣  Testando análise de balanceamento...")
    balance = analyzer.analyze_balance()
    print(f"   Score de balanceamento: {balance['balance_score']}")
    print(f"   Folhas: {balance['leaf_nodes']}")
    print(f"   Braço mais longo: {balance['longest_branch']['from']} → {balance['longest_branch']['to']}")
    
    print("\n✅ Todos os testes individuais concluídos!")

if __name__ == "__main__":
    # Executar testes
    test_individual_metrics()
    test_with_different_graphs()
    
    print("\n" + "="*80)
    print("TODOS OS TESTES CONCLUÍDOS!")
    print("="*80 + "\n")