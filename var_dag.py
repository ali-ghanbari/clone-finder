from typing import List, Set

from parsing.ast.goal_ast import Var


class VarDAG:
    def __init__(self):
        self.__adj = {}
        self.__visited = set()
        self.__topo_sort_res = []

    def add_node(self, node : Var):
        if node not in self.__adj:
            self.__adj[node] = []

    def add_edge(self, src : Var, dst : Var):
        self.add_node(src)
        self.add_node(dst)
        self.__adj[src].append(dst)

    def __dfs_visit(self, node : Var, local_visited : Set[Var]):
        self.__visited.add(node)
        local_visited.add(node)
        for v in self.__adj[node]:
            if v not in self.__visited:
                self.__dfs_visit(v, local_visited)
            elif v in local_visited:
                raise ValueError('Not a DAG')
        self.__topo_sort_res.insert(0, node)
        local_visited.remove(node)


    def get_topological_ordering(self) -> List[Var]:
        self.__topo_sort_res.clear()
        self.__visited.clear()
        for node in self.__adj:
            if node not in self.__visited:
                self.__dfs_visit(node, set())
        return self.__topo_sort_res
