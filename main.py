from utils.loader import load_graph
from analysis.compare import compare

graph = load_graph("data/bairros.json")
result = compare(graph)

for alg, data in result.items():
    print(f"{alg}:")
    print(f"  Custo total: {data['cost']}")
    print(f"  Tempo: {data['time']:.6f}s\n")
