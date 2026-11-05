# python3 Main.py < _in.txt > _solver.txt

import sys

from Graph import Graph as g
from Graph import Arc as a
import Solve as s

#--------- Funções ---------#

def normaliza_min_alvo_a_max_alvo(vals, min_alvo, max_alvo):
    val_min = min(vals)
    val_max = max(vals)

    if val_max == val_min:
        return [1.0 for _ in vals]

    return [min_alvo + (max_alvo - min_alvo) * (val - val_min) / (val_max - val_min) for val in vals]

#--------- Globais ---------#

_out = open("_out.txt","w")

#--------- Leitura da Entrada ---------#

input_data = sys.stdin.read().split()
it = iter(input_data)

I_count = int(next(it))
instances = []
for _ in range(I_count):
    inst = []
    val = int(next(it))
    while val != 0:
        inst.append(val)
        val = int(next(it))
    instances.append(inst)

#_out.write(f"{instances}\n")

V_count = int(next(it))
O_count = int(next(it))

r = 0 # Vértice Artificial Raiz
G = g(V_count)
G.add_node(r, 0.0)

# Processa todas as operacoes do grafo.
lista_v = []
lista_w_val_vert = []
lista_arc = []
lista_w_val_arc = []
lista_custo = [0]*(V_count+1)

for _ in range(O_count):
    op = next(it)

    if op == 'W':
        v = int(next(it))
        w_val = float(next(it))
        G.set_node_weight(v, w_val)

        lista_v.append(v)
        lista_w_val_vert.append(w_val)  
        continue

    if op == 'I':
        v1 = int(next(it))
        v2 = int(next(it))
        w_val = int(next(it))
        G.insert_arc(a(v1, v2, w_val))

        lista_arc.append((v1, v2))
        lista_w_val_arc.append(w_val)

#--------- Formatação para o PLI ---------#

# Normalização dos Prêmios
P0 = dict(zip(lista_v, lista_w_val_vert))

min_alvo_norm = 1e-2
max_alvo_norm = 1e14

lista_w_val_norm = normaliza_min_alvo_a_max_alvo(lista_w_val_vert, min_alvo_norm, max_alvo_norm)
for v, w_val_norm in zip(lista_v, lista_w_val_norm):
    G.set_node_weight(v, w_val_norm)
    #_out.write(f"Prêmio normalizado[{v}]: {w_val_norm}\n")

# Normalização dos Custos
W0 = dict(zip(lista_arc, lista_w_val_arc))

min_alvo_norm = 1e-2
max_alvo_norm = 1e14

lista_w_val_norm = normaliza_min_alvo_a_max_alvo(lista_w_val_arc, min_alvo_norm, max_alvo_norm)
for e, w_val_norm in zip(lista_arc, lista_w_val_norm):
    G.set_arc_weight(a(e[0], e[1], w_val_norm))
    #_out.write(f"Custo normalizado[{(e[0], e[1])}]: {w_val_norm}\n")

    if not lista_custo[e[1]]:
        lista_custo[e[1]] = w_val_norm

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

_out.write("\nGrafo:\n")
_out.write(f"- Vértices (V): {len(V)}\n")
_out.write(f"- Arestas (A): {len(A)}\n")
_out.write(f"- Raiz (r): {r}\n\n")

for i in range(I_count):

    # Orçamento
    n = 0
    for j in instances[i]:
        n += lista_custo[j]

    _out.write(f"Instancia_{i}:\n")
    _out.write(f"Orçamento: {n}\n")
    s.optimize_skill_tree(V,A,R,r,P,P0,W,W0,n,_out)
    _out.write("\n")