# python3 Main.py {budget} < _in.txt > _out.txt
# substituir {budget} pela quantidade de heavenly chips ou apaga-lo para usar o padrão

import sys

from Graph import Graph as g
from Graph import Arc as a
import Solve as s

#--------- Argumentos/Globais ---------#

# Orçamento
ORCAMENTO = 1_000_000_000_000_000.0
n = float(sys.argv[1]) if len(sys.argv) > 1 else ORCAMENTO

#--------- Leitura da Entrada ---------#

input_data = sys.stdin.read().split()
it = iter(input_data)

V_count = int(next(it))
O_count = int(next(it))

r = 0 # Vértice Artificial Raiz
G = g(V_count)
G.add_node(r, 0.0)

# Processa todas as operacoes do grafo.
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

#--------- Formatação para o PLI ---------#

# Vértices e Pesos/Prêmios
V = [v for v in G.adj_list if v != r]
P = {v: G.get_node_weight(v) for v in V}

# Arestas e Pesos/Custos do grafo.
A = []
W = {}
for u in G.adj_list:
    for elem in G.adj_list[u]:
        e = (u, elem.destiny)
        A.append(e)
        W[e] = elem.weight

# Arestas Artificiais
R = []
for v in V:
    if v == 1:
        continue
    e = (r, v)
    R.append(e)
    W[e] = 0.0 

#--------- Chamada do PLI ---------#

print("\n------------------------------------\n")
print("Executando Otimização...")
print(f"- Vértices (V): {len(V)}")
print(f"- Arestas (A): {len(A)}")
print(f"- Raiz (r): {r}")
print(f"- Orçamento (n): {n}\n")

#modelo, x_vars, selected_edges, total_prize, total_cost = 
s.optimize_skill_tree(V,A,R,r,P,W,n)
