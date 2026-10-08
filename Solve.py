from pyscipopt import Model, quicksum

def optimize_skill_tree(V, A, R, r, P, W, n):

    modelo = Model("CookieClicker_PrizeCollecting")

    #--------- Parametros ---------#

    E = A + R
    k = len(V)

    y = {} # y[v] = 1 se for Aresta Real, 0 se for Aresta Artificial
    for e in E:
        y[e] = 0
        if e in A:
            y[e] = 1

    #--------- Váriaveis ---------#

    x = {} # x[v] = 1 se a melhoria v foi comprada/coletada.
    for v in V:
        x[v] = modelo.addVar(vtype="B", name=f"x_{v}")

    z = {} # z[e] = 1 se a aresta fizer parte da progressão adquirida
    for e in E:
        z[e] = modelo.addVar(vtype="B", name=f"z_{e[0]}_{e[1]}")

    f = {} # f[e]: fluxo na aresta e
    for e in E:
        f[e] = modelo.addVar(vtype="C", lb=0, name=f"f_{e[0]}_{e[1]}")

    #--------- Função Objetivo ---------#

    # Maximiza os Prêmios(pesos dos vértices)
    modelo.setObjective(
        quicksum(P[v] * z[(u,v)] * y[(u,v)] for (u,v) in A),
        sense="maximize",
    )

    #--------- Restrições ---------#

    # 1. Orçamento
    # O custo total não pode passar de 'n'
    modelo.addCons(
        quicksum(W[e] * z[e] for e in A) <= n,
        name="c1_budget",
    )

    # 2. Raiz envia k unidades de fluxo
    modelo.addCons(
        quicksum(f[e] for e in E if e[0] == r) == k,
        name="c2_root_flow"
    )

    # 3. Cada vértice consome exatamente 1 unidade
    for v in V:
        modelo.addCons(quicksum(f[e] for e in E if e[1] == v) == quicksum(f[e] for e in E if e[0] == v)+1,
            name=f"c3_flow_conservation_{v}"
        )

    # 4. Só passa fluxo em arco ativo
    for e in E:
        modelo.addCons(f[e] <= k * z[e],
            name=f"c4_flow_capacity_{e[0]}_{e[1]}"
        )

    # 5. Arcos artificiais
    for r, u in R:
        for i, j in A:
            if u == i:
                modelo.addCons(
                    z[(i, j)] <= 1 - z[(r, i)],
                    name=f"c5_artificial_edge_{i}_{j}"
                )

    # 6. Vértice ligado por arco artificial não pode ter filhos
    for i, j in R:
        for i_, j_ in A:
            if i_ == j:
                modelo.addCons(
                    z[(i_, j_)] <= 1 - z[(i, j)],
                    name=f"c6_exclusion_{j}_{j_}"
                )

    # 7. Cada vértice só pode ter exatamente um pai na solução
    for v in V:
        if v != r:
            modelo.addCons(
                quicksum(z[e] for e in E if e[1] == v) == 1,
                name=f"c7_in_degree_{v}"
            )

    # 8. Dependência dos vértices antecessores (pré-requisito)
    for i, j in A:
        if i != r:
            modelo.addCons(
                x[j] <= x[i],
                name=f"c8_prerequisite_{i}_{j}"
            )

    # 9. Se uma aresta ij for escolhida, o vértice j tem que ser coletado
    for j in V:
        if j != r:
            modelo.addCons(
                quicksum(z[e] for e in E if e[1] == j) <= x[j],
                name=f"c9_link_{j}"
            )

    # 10. Apenas um arco Real saindo da raiz
    real_root_arcs = [
        e for e in A
        if e[0] == r
    ]

    if real_root_arcs:
        modelo.addCons(
            quicksum(z[e] for e in real_root_arcs) == 1,
            name="c10_root_real_degree"
        )
    
    #--------- Otimização ---------#

    modelo.writeProblem("modelo.lp")
    modelo.optimize()

    status = modelo.getStatus()
    print(f"Status do modelo: {status}")

    if modelo.getNSols() == 0:
        print("Nenhuma solução viável encontrada")
        return modelo, {}, {}, {}, 0.0, 0.0

    #--------- Solução ---------#

    x_sol = {v: int(modelo.getVal(x[v]) > 0.5) for v in V}
    z_sol = {e: int(modelo.getVal(z[e]) > 0.5) for e in E}

    selected_vertices = [v for v in V if x_sol[v] == 1]
    selected_real_edges = [e for e in A if z_sol[e] == 1]
    selected_artificial_edges = [e for e in R if z_sol[e] == 1]

    total_prize = sum(float(P.get(v, 0.0)) for v in selected_vertices)
    total_cost = sum(float(W[(u, v)]) for (u, v) in selected_real_edges)

    print(f"Prêmio total: {total_prize:.10g}")
    print(f"Custo total: {total_cost:.10g}")
    print()

    print(f"Vértices adquiridos({len(selected_vertices)}):")
    for v in selected_vertices:
        print(f"  {v} (prêmio={P.get(v, 0.0)})")
    print()

    print(f"Arestas Reais adquiridas({len(selected_real_edges)}):")
    for u, v in selected_real_edges:
        print(f"  ({u}, {v}) (custo={W[(u, v)]})")
    print()
    
    print(f"Arestas Artificiais adquiridas({len(selected_artificial_edges)}):")
    for u, v in selected_artificial_edges:
        print(f"  ({u}, {v}) (custo={W[(u, v)]})")

    return modelo, x_sol, z_sol, selected_real_edges, total_prize, total_cost
