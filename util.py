from collections import deque

from parsing.ast.goal_ast import Term, Product, Var
from parsing.goal_parser import GoalParser
from proof_tree import ProofTree
from var_dag import VarDAG


# def topological_sort(local_context, defined_vars):
#     relevant_vars = {var: local_context[var][1] & defined_vars for var in defined_vars if var in local_context}
#
#     graph = {var: set() for var in relevant_vars}  # Only include relevant variables
#     in_degree = {var: 0 for var in relevant_vars}
#
#     for var, deps in relevant_vars.items():
#         for dep in deps:
#             if dep in graph:  # Only add edges within vars_to_sort
#                 graph[dep].add(var)
#                 in_degree[var] += 1
#     queue = deque([var for var in defined_vars if in_degree.get(var, 0) == 0])
#     sorted_order = []
#     while queue:
#         var = queue.popleft()
#         sorted_order.append(var)
#         for neighbor in graph.get(var, []):
#             in_degree[neighbor] -= 1
#             if in_degree[neighbor] == 0:
#                 queue.append(neighbor)
#     return sorted_order


def make_dag(locally_defined_fvs, local_context):
    dag = VarDAG()
    for s in locally_defined_fvs:
        dag.add_node(s)
        for d in local_context[s][1]:
            if d in local_context: # only keep those variables that are locally defined
                dag.add_edge(s, d)
    return dag

def generalize(proof_tree: ProofTree, goal : str):
    local_context = dict()
    for d in proof_tree.get_local_context(goal):
        index_of_colon = d.index(':')
        defn_body = d[index_of_colon + 1:].strip()
        for defn_var in d[:index_of_colon].split(','):
            defn_var = defn_var.strip()
            local_context[Var(defn_var)] = (defn_body, GoalParser(defn_body).parse().free_vars())
    locally_defined_fvs = set()
    for fv in GoalParser(goal).parse().free_vars():
        if fv in local_context:
            locally_defined_fvs.add(fv)
    dag = make_dag(locally_defined_fvs, local_context)
    rev_top_order = dag.get_topological_ordering()
    # rev_top_order = topological_sort(local_context, locally_defined_fvs)
    rev_top_order.reverse()
    for fv in rev_top_order:
        goal = 'forall (%s : %s), (%s)' % (fv, local_context[fv][0], goal)
    return goal


def is_prod_body(p : Term, t : Term) -> bool:
    while isinstance(p, Product):
        p = p.get_body()
        if p == t:
            return True
    return False
