from dataclasses import dataclass
from typing import Dict, List, Optional

class Arc:
    def __init__(self, v1: int, v2: int, w: float = 1.0):
        self.v1 = v1
        self.v2 = v2
        self.w = w

@dataclass
class AdjElement:
    destiny: int
    weight: float

class Graph:
    def __init__(self, num_nodes: int = 0):
        self.num_nodes = 0
        self.num_arcs = 0
        self.adj_list: Dict[int, List[AdjElement]] = {}
        self.node_weights: Dict[int, float] = {}
        self._next_node_id = 0

        for _ in range(num_nodes):
            self.add_node()

    #--------- Vértices/Nodos ---------#

    def add_node(self, v: Optional[int] = None, w: float = 0.0) -> int:
        if v is None:
            v = self._next_node_id
            while v in self.adj_list:
                v += 1
            self._next_node_id = v + 1

        if v not in self.adj_list:
            self.adj_list[v] = []
            self.node_weights[v] = w
            self.num_nodes += 1
        else:
            self.node_weights[v] = w

        return v

    def remove_node(self, v: int) -> None:
        if v not in self.adj_list:
            return
        
        # Remove arestas de Saida
        self.num_arcs -= len(self.adj_list[v])
        del self.adj_list[v]
        del self.node_weights[v]

        # Remove arestas de Entrada
        for u in self.adj_list:
            len_antes = len(self.adj_list[u])
            self.adj_list[u] = [elem for elem in self.adj_list[u] if elem.destiny != v]
            self.num_arcs -= (len_antes - len(self.adj_list[u]))

        self.num_nodes -= 1

    def set_node_weight(self, v: int, w: float) -> None:
        if v in self.node_weights:
            self.node_weights[v] = w

    def get_node_weight(self, v: int) -> float:
        return self.node_weights.get(v, 0.0)

    #--------- Arcos/Arestas ---------#

    def insert_arc(self, e: Arc) -> None:
        if e.v1 in self.adj_list and e.v2 in self.adj_list:
            self.adj_list[e.v1].insert(0, AdjElement(e.v2, e.w))
            self.num_arcs += 1

    def remove_arc(self, e: Arc) -> None:
        if e.v1 in self.adj_list:
            for elem in self.adj_list[e.v1]:
                if elem.destiny == e.v2:
                    self.adj_list[e.v1].remove(elem)
                    self.num_arcs -= 1
                    break

    def set_arc_weight(self, e: Arc) -> None:
        for elem in self.adj_list[e.v1]:
            if elem.destiny == e.v2:
                elem.weight = e.w
                return

    def get_arc_weight(self, e: Arc) -> float:
        if e.v1 in self.adj_list:
            for elem in self.adj_list[e.v1]:
                if elem.destiny == e.v2:
                    return elem.weight

