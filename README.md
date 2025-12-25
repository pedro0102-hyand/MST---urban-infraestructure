# 🌳 Projeto de Árvore Geradora Mínima (MST)

## 📋 Sobre o Projeto

Este projeto implementa e compara os dois principais algoritmos para encontrar a **Árvore Geradora Mínima** (Minimum Spanning Tree - MST) em grafos: **Prim** e **Kruskal**. O contexto é a otimização de redes de conexão entre bairros, minimizando o custo total de infraestrutura.

### 🎯 Objetivos

- Implementar os algoritmos de Prim e Kruskal
- Comparar desempenho e resultados
- Visualizar o processo passo a passo
- Analisar métricas avançadas da MST (diâmetro, raio, centro, balanceamento)

---

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd projeto-mst

# Instale as dependências
pip install -r requirements.txt
```

### Executando o Projeto

```bash
# Análise principal com visualizações
python main.py

# Testes detalhados das métricas
python test_metrics.py
```

### Saída Esperada

Após executar `main.py`, você verá:
- Comparação de tempo e custo entre Prim e Kruskal
- Arquivos gerados na pasta `results/`:
  - `grafo_original.png` - Visualização do grafo completo
  - `prim_animation.gif` - Animação do algoritmo de Prim
  - `kruskal_animation.gif` - Animação do algoritmo de Kruskal

---

## 📁 Estrutura do Projeto

```
projeto-mst/
│
├── algorithms/              # Implementação dos algoritmos
│   ├── prim.py             # Algoritmo de Prim
│   ├── kruskal.py          # Algoritmo de Kruskal
│   └── union_find.py       # Estrutura Union-Find para Kruskal
│
├── analysis/               # Análise e comparação
│   ├── compare.py          # Comparação de desempenho
│   └── mst_metrics.py      # Métricas avançadas da MST
│
├── data/                   # Dados de entrada
│   ├── bairros.json        # Grafo pequeno (5 vértices)
│   └── bigger.json         # Grafo maior (10 vértices)
│
├── graph/                  # Estruturas de dados
│   ├── graph.py            # Classe Graph
│   └── edge.py             # Classe Edge
│
├── utils/                  # Utilitários
│   ├── __init__.py
│   └── loader.py           # Carregador de grafos JSON
│
├── results/                # Saída das visualizações (gerado automaticamente)
│
├── visualize.py            # Geração de visualizações
├── main.py                 # Script principal
├── test_metrics.py         # Testes das métricas
├── requirements.txt        # Dependências do projeto
└── README.md              # Este arquivo
```

---

## 🔬 Algoritmos Implementados

### 1. Algoritmo de Prim

**Estratégia**: Cresce a árvore a partir de um vértice inicial, sempre escolhendo a aresta de menor peso que conecta um vértice visitado a um não visitado.

**Características**:
- Usa fila de prioridade (heap)
- Complexidade: O(E log V)
- Ideal para grafos densos
- Sempre começa de um vértice específico

**Pseudocódigo**:
```
1. Inicia no vértice escolhido
2. Adiciona todas arestas adjacentes na fila de prioridade
3. Repete até visitar todos os vértices:
   - Remove aresta de menor peso da fila
   - Se o destino não foi visitado:
     * Adiciona à MST
     * Marca vértice como visitado
     * Adiciona novas arestas adjacentes à fila
```

### 2. Algoritmo de Kruskal

**Estratégia**: Ordena todas as arestas por peso e adiciona uma a uma à MST, desde que não forme ciclos.

**Características**:
- Usa estrutura Union-Find para detectar ciclos
- Complexidade: O(E log E)
- Ideal para grafos esparsos
- Trabalha com todas as arestas ordenadas

**Pseudocódigo**:
```
1. Ordena todas as arestas por peso crescente
2. Para cada aresta (u, v):
   - Se u e v estão em componentes diferentes:
     * Adiciona aresta à MST
     * Une os componentes de u e v
   - Senão, descarta (formaria ciclo)
```

### 3. Union-Find (Disjoint Set)

Estrutura de dados auxiliar para Kruskal que mantém componentes conexos:
- `find(v)`: Encontra o representante do conjunto de v (com compressão de caminho)
- `union(u, v)`: Une dois conjuntos; retorna True se estavam separados

---

## 📊 Métricas Avançadas da MST

O módulo `analysis/mst_metrics.py` calcula métricas importantes para análise de redes:

### 🎯 Conceitos Fundamentais

#### Excentricidade de um Vértice
Maior distância daquele vértice para qualquer outro vértice da árvore.

**Exemplo**:
```
    A --- B --- C --- D --- E
    
    exc(A) = 4 (distância até E)
    exc(B) = 3 (distância até E)
    exc(C) = 2 (distância até A ou E) ← menor!
```

#### Raio da MST
Menor excentricidade entre todos os vértices. Indica o melhor local para centralizar serviços.

```
Raio = min(todas as excentricidades)
```

**Interpretação**: Se você instalar uma central no vértice com menor excentricidade (centro), essa é a distância máxima que qualquer bairro ficará.

#### Diâmetro da MST
Maior distância entre quaisquer dois vértices. Indica o "comprimento" total da rede.

```
Diâmetro = max(distância(u, v) para todos u, v)
```

**Interpretação**: Pior cenário de comunicação entre dois pontos extremos da rede.

#### Centro da MST
Vértice(s) com excentricidade igual ao raio. Localização ótima para centralização.

### 📐 Relações Importantes

```
Raio ≤ Diâmetro ≤ 2 × Raio

Se Diâmetro ≈ 2 × Raio → Árvore balanceada ✅
Se Diâmetro >> 2 × Raio → Árvore alongada ⚠️
```

### ⚖️ Análise de Balanceamento

- **Vértices folha**: Grau 1 (extremidades da rede)
- **Vértices internos**: Grau > 1 (pontos de distribuição)
- **Grau médio**: Indica complexidade da rede
- **Score de balanceamento**: 0-1, baseado na variância dos graus

---

## 📈 Formato dos Dados de Entrada

Os grafos são armazenados em arquivos JSON com o seguinte formato:

```json
[
    ["Vértice1", "Vértice2", peso],
    ["Centro", "Bairro A", 4],
    ["Centro", "Bairro B", 3],
    ["Bairro A", "Bairro B", 2]
]
```

### Grafos Disponíveis

**`data/bairros.json`** - Grafo pequeno
- 5 vértices (Centro, Bairros A-D)
- 7 arestas
- Ideal para testes rápidos

**`data/bigger.json`** - Grafo maior
- 10 vértices (Centro, Bairros A-J)
- 18 arestas
- Para análises mais complexas

### Criando Seus Próprios Grafos

Crie um arquivo JSON seguindo o formato acima e carregue-o usando:

```python
from utils.loader import load_graph

graph = load_graph("data/seu_grafo.json")
```

---

## 🎨 Visualizações

### Esquema de Cores

- 🟢 **Verde**: Arestas que fazem parte da MST
- 🟡 **Amarelo tracejado**: Aresta sendo considerada no momento
- ⚪ **Cinza claro**: Arestas não utilizadas na MST
- 🔵 **Azul**: Vértices visitados
- ⚪ **Branco/Cinza**: Vértices não visitados

### Tipos de Visualização

1. **Grafo Original** (PNG estático)
   - Mostra todas as conexões possíveis
   - Pesos das arestas
   - Layout otimizado para visualização

2. **Animação Prim** (GIF)
   - Mostra o crescimento da árvore passo a passo
   - Destaca a aresta sendo adicionada
   - Exibe custo acumulado

3. **Animação Kruskal** (GIF)
   - Mostra arestas sendo testadas em ordem de peso
   - Indica aceitação (não forma ciclo) ou rejeição
   - Exibe custo acumulado

---

## 🧪 Testes e Validação

### Executar Testes Básicos

```bash
python test_metrics.py
```

### O que é Testado

1. **Testes individuais de métricas**:
   - Cálculo de diâmetro
   - Cálculo de centro e raio
   - Análise de balanceamento

2. **Testes com diferentes grafos**:
   - Validação de que Prim e Kruskal encontram o mesmo custo
   - Análise completa de métricas
   - Comparação entre grafos pequenos e grandes

### Saída dos Testes

```
🧪🧪🧪🧪 TESTE INDIVIDUAL DE MÉTRICAS 🧪🧪🧪🧪

MST de teste:
  A - B (peso: 1)
  B - C (peso: 2)
  C - D (peso: 1)
  B - E (peso: 3)

1️⃣  Testando cálculo de diâmetro...
   Diâmetro: 6
   Entre: ('A', 'E')

2️⃣  Testando cálculo de centro e raio...
   Centro: B
   Raio: 3

3️⃣  Testando análise de balanceamento...
   Score de balanceamento: 0.560
   Folhas: ['A', 'D', 'E']
   Braço mais longo: B → E
```

---

## 💡 Aplicações Práticas

### 1. Planejamento Urbano
- Otimizar redes de água, energia ou esgoto
- Minimizar custos de infraestrutura
- Identificar localizações centrais para serviços públicos

### 2. Redes de Telecomunicações
- Design de redes de fibra ótica
- Minimizar cabeamento
- Identificar pontos críticos (alta excentricidade)

### 3. Transporte e Logística
- Planejamento de rotas de distribuição
- Otimização de linhas de ônibus/metrô
- Identificar hubs estratégicos

### 4. Análise de Redes Sociais
- Identificar pessoas centrais (baixa excentricidade)
- Medir "diâmetro" da rede social
- Análise de comunidades

---

## 📚 Conceitos de Teoria dos Grafos

### Árvore Geradora
Subgrafo que:
- Conecta todos os vértices
- Não possui ciclos
- É uma árvore (V-1 arestas para V vértices)

### Árvore Geradora Mínima (MST)
Árvore geradora com a **menor soma de pesos** possível.

**Propriedades**:
- Única (geralmente) para grafos com pesos distintos
- Múltiplas possíveis se há arestas com pesos iguais
- Conecta todos os vértices com custo mínimo

### Complexidade Computacional

| Algoritmo | Complexidade | Melhor para |
|-----------|--------------|-------------|
| Prim | O(E log V) | Grafos densos |
| Kruskal | O(E log E) | Grafos esparsos |

Onde:
- V = número de vértices
- E = número de arestas

---

## 🔧 Dependências

```
matplotlib>=3.5.0    # Visualizações e gráficos
networkx>=2.6.0      # Manipulação de grafos
Pillow>=9.0.0        # Geração de GIFs
```

---

## 📖 Exemplos de Uso Avançado

### Análise Personalizada

```python
from utils.loader import load_graph
from algorithms.prim import prim
from analysis.mst_metrics import MSTAnalyzer

# Carregar grafo
graph = load_graph("data/bairros.json")

# Executar Prim
start = "Centro"
mst_edges, cost = prim(graph, start)

# Analisar métricas
analyzer = MSTAnalyzer(mst_edges)
analysis = analyzer.get_full_analysis()

# Acessar métricas específicas
print(f"Diâmetro: {analysis['diameter']['diameter']}")
print(f"Centro: {analysis['center_and_radius']['center']}")
print(f"Raio: {analysis['center_and_radius']['radius']}")

# Imprimir análise completa formatada
analyzer.print_analysis()
```

### Comparação de Algoritmos

```python
from utils.loader import load_graph
from analysis.compare import compare

graph = load_graph("data/bigger.json")
results = compare(graph)

for algorithm, metrics in results.items():
    print(f"{algorithm}:")
    print(f"  Custo: {metrics['cost']}")
    print(f"  Tempo: {metrics['time']:.6f}s")
```

### Criar Visualizações Personalizadas

```python
from utils.loader import load_graph
from visualize import (
    visualize_original_graph,
    visualize_prim_gif,
    visualize_kruskal_gif
)

graph = load_graph("data/seu_grafo.json")

# Gerar apenas o grafo original
visualize_original_graph(graph, "meu_grafo.png")

# Gerar apenas animação do Prim
visualize_prim_gif(graph, start_vertex="Centro", filename="meu_prim.gif")

# Gerar apenas animação do Kruskal
visualize_kruskal_gif(graph, filename="meu_kruskal.gif")
```



```bash
# Certifique-se de que as dependências estão instaladas
pip install -r requirements.txt
```

### Erro ao carregar arquivo JSON

```python
# Verifique o formato do JSON
# Deve ser uma lista de listas: [["A", "B", peso], ...]
```

### Visualizações não aparecem

```bash
# No Linux, pode ser necessário instalar tkinter
sudo apt-get install python3-tk

# No macOS
brew install python-tk
```

### GIF não é gerado

```bash
# Reinstale Pillow
pip uninstall Pillow
pip install Pillow
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

