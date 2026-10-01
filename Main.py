# python3 Main.py {budget} < _in.txt > _out.txt
# substituir {budget} pela quantidade de heavenly chips ou apaga-lo para usar o padrão

import sys
from Graph import Graph as g
from Graph import Arc as a
import Solve as s

# Leitura da entrada
input_data = sys.stdin.read().split()
it = iter(input_data)

V_count = int(next(it))
O_count = int(next(it))

print(f"Nodes: {V_count}")
print(f"Operations: {O_count}\n")

G = g(V_count)

# Processa todas as operações de carregamento do grafo
for _ in range(O_count):
    op = next(it)

    if op == 'W':
        v = int(next(it))
        w_val = float(next(it))
        G.set_node_weight(v, w_val)
        continue

    if op == 'I':
        v1 = int(next(it))
        v2 = int(next(it))
        w_val = float(next(it))
        G.insert_arc(a(v1, v2, w_val))

#---------Formatação dos Dados para o PLI---------#

# Identificador do nó artificial raiz
r = 0

# Lista de vértices reais e conjunto total V (isso inclui o r)
real_nodes = list(G.adj_list.keys())
V = real_nodes

# Conjunto de Arestas Reais (A) e Dicionário de Pesos/Custos (w)
A = []
W = {}

for u in G.adj_list:
    for elem in G.adj_list[u]:
        e = (u, elem.destiny)
        A.append(e)
        W[e] = elem.weight

# Conjunto de Arestas Artificiais (R) saindo da raiz 'r'
R = [(r, v) for v in real_nodes]
for e in R:
    W[e] = 0.0

# Dicionário de Prêmios/Pesos dos Vértices (p)
P = {v: G.get_node_weight(v) for v in real_nodes}

# Orçamento máximo (n)
n = float(sys.argv[1]) if len(sys.argv) > 1 else 1000000.0

print(f"Executando Otimização...")
print(f"- Total de Vértices (V): {len(V)}")
print(f"- Arestas Reais (A): {len(A)}")
print(f"- Arestas Artificiais (R): {len(R)}")
print(f"- Orçamento (n): {n}\n")

# --------- Chamada do Modelo de Otimização --------- #

modelo, x_vars, z_vars = s.optimize_skill_tree(V, A, R, r, P, W, n)