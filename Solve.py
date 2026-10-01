from pyscipopt import Model, quicksum

def optimize_skill_tree(V, A, R, r, P, W, n):

    # Inicia o SCIP
    modelo = Model("SkillTree_PLI")

    # Cria parametros
    E = A + R
    y = {e: 1 if e in A else 0 for e in E}
    k = len(V)-1

    #--------- Váriaveis ---------#

    x = {} # x_v: se o vértice v foi coletado
    for v in V:
        if v != r:
            x[v] = modelo.addVar(vtype="B", name=f"x_{v}")

    z = {} # z_e: se a aresta e foi escolhida
    for e in E:
        z[e] = modelo.addVar(vtype="B", name=f"z_{e[0]}_{e[1]}")

    f = {} # f_e: fluxo na aresta e
    for e in E:
        f[e] = modelo.addVar(vtype="C", lb=0, name=f"f_{e[0]}_{e[1]}")

    #--------- Função Objetivo ---------#

    # 0. Maximiza o prêmio dos vértices coletados se não for artificial
    modelo.setObjective(
        quicksum(P[j] * z[(i, j)] * y[(i, j)] for (i, j) in A),
        sense="maximize"
    )

    #--------- Restrições ---------#
    
    # 1. Limita o custo total das arestas
    modelo.addCons(
        quicksum(W[e] * z[e] for e in A) <= n,
        name="c1_budget"
    )

    # 2. Raiz envia k unidades de fluxo
    modelo.addCons(
        quicksum(f[e] for e in E if e[0] == r) == k,
        name="c2_root_flow"
    )

    # 3. Cada vértice consome 1 unidade de fluxo
    for v in V:
        if v != r:
            modelo.addCons(
                quicksum(f[e] for e in E if e[0] == v) == quicksum(f[e] for e in E if e[1] == v) - 1,
                name=f"c3_flow_conservation_{v}"
            )

    # 4. Só passa fluxo em arco escolhido, limitado a k
    for e in E:
        modelo.addCons(
            f[e] <= z[e] * k,
            name=f"c4_flow_capacity_{e[0]}_{e[1]}"
        )

    # 5. Vértice ligado por arco artificial à raiz não pode ter filhos
    for i in V:
        if i != r and (r, i) in R:
            for j in V:
                if (i, j) in A:
                    modelo.addCons(
                        z[(i, j)] <= 1 - z[(r, i)],
                        name=f"c5_exclusion_{i}{j}"
                    )

    # 6. Cada vértice só pode ter exatamente um pai na solução
    for v in V:
        if v != r:
            modelo.addCons(
                quicksum(z[e] for e in E if e[1] == v) <= 1,
                name=f"c6_in_degree_{v}"
            )

    # 7. A raiz possui exatamente um filho
    modelo.addCons(
        quicksum(z[e] for e in E if e[0] == r) == 1,
        name="c7_root_out_degree"
    )

    # 8. Dependência dos vértices antecessores
    for v in V:
        if v != r:
            ancestors = [i for (i, j) in A if j == v]
            if ancestors:
                modelo.addCons(
                    quicksum(x[i] for i in ancestors) >= x[v] * len(ancestors),
                    name=f"c8_ancestors_{v}"
                )

    # 9. Se uma aresta ij for escolhida, o vértice j tem que ser coletado
    for j in V:
        if j != r:
            modelo.addCons(
                quicksum(z[e] for e in E if e[1] == j) <= x[j],
                name=f"c9_link_{j}"
            )

    #--------- Otimização ---------#

    modelo.optimize()

    if modelo.getStatus() == "optimal":
        print("Solução ótima encontrada.")
    else:
        print("Solução não ótima.")
    
    # Imprime as arestas escolhidas
    for e in A:
        if modelo.getVal(z[e]) > 0.5:
            print(f"Aresta escolhida: {e}")

    return modelo, x, z