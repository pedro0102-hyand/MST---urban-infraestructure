from utils.loader import load_graph
from analysis.compare import compare
from visualize import generate_all_visualizations

def main():
    print("\n" + "="*60)
    print("ANÁLISE DE ÁRVORE GERADORA MÍNIMA")
    print("="*60)
    
    # Carregar grafo
    print("\n1. Carregando grafo...")
    graph = load_graph("data/bairros.json")
    print(f"   ✓ Grafo carregado com {len(graph.edges)} arestas")
    
    # Comparar algoritmos
    print("\n2. Comparando algoritmos...")
    result = compare(graph)
    
    print("\n" + "-"*60)
    print("RESULTADOS DA COMPARAÇÃO")
    print("-"*60)
    for alg, data in result.items():
        print(f"\n{alg}:")
        print(f"  Custo total: {data['cost']}")
        print(f"  Tempo: {data['time']:.6f}s")
    print("-"*60)
    
    # Gerar visualizações
    print("\n3. Gerando visualizações...")
    generate_all_visualizations(graph)
    
    print("\n" + "="*60)
    print("PROCESSO CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\nPara visualizar:")
    print("  - Abra results/grafo_original.png")
    print("  - Abra results/prim_animation.gif")
    print("  - Abra results/kruskal_animation.gif")
    print()

if __name__ == "__main__":
    main()
