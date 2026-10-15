# python3 Main.py < _in.txt > _solver.txt

import sys

from Graph import Graph as g
from Graph import Arc as a
import Solve as s

#--------- Argumentos/Globais ---------#

_out = open("_out.txt","w")
_out.write("\n")

#--------- Leitura da Entrada ---------#

input_data = sys.stdin.read().split()
it = iter(input_data)

I_count = int(next(it))
instances = []
for _ in range(I_count):
    instances.append(int(next(it)))

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
        G.set_node_weight(v, w_val+1) #+1 só pra n ter ganho zerado
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

_out.write("Grafo:\n")
_out.write(f"- Vértices (V): {len(V)}\n")
_out.write(f"- Arestas (A): {len(A)}\n")
_out.write(f"- Raiz (r): {r}\n\n")

for i in range(I_count):
    n = instances[i]
    _out.write(f"Instancia_{i}:\n")
    _out.write(f"Orçamento: {n}\n")
    s.optimize_skill_tree(V,A,R,r,P,W,n,_out)
    _out.write("\n")
