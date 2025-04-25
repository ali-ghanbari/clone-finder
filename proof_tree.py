import glob
import os
import re
from typing import List, Set

from coqpyt.coq.proof_file import ProofFile


class ProofTree:
    def __init__(self, theorem_name : str):
        self.__tree = {}
        self.__theorem_name = theorem_name

    def __add_node(self, node : str,
                   locally_defined_symbols : List[str],
                   local_context : List[str],
                   children : List[str],
                   tactic : str):
        self.__tree[node] = {
            'locally defined symbols': locally_defined_symbols,
            'local context': local_context,
            'children': children,
            'tactic': tactic
        }

    def __get_proof(self, node : str, acc : List[str], visited : Set[str]):
        if node not in self.__tree:
            return
        if node in visited: # sometimes a tactic results in the same goal, leading to a loop
            return
        m = self.__tree[node]
        acc.append(m['tactic'])
        visited.add(node)
        for child in m['children']:
            self.__get_proof(child, acc, visited)

    def get_proof(self, node : str) -> List[str]:
        result = []
        self.__get_proof(node, result, set())
        return result

    def get_local_context(self, node : str) -> List[str]:
        return self.__tree[node]['local context']

    def get_locally_defined_symbols(self, node : str) -> List[str]:
        return self.__tree[node]['locally defined symbols']

    def get_nodes(self) -> List[str]:
        return list(self.__tree.keys())

    def get_theorem_name(self) -> str:
        return self.__theorem_name

    def __repr__(self):
        return str(self.__tree)

    @staticmethod
    def print_errors(errors):
        if len(errors) > 0:
            print('*' * 50)
            for error in errors:
                print(error.message)
            print('*' * 50)

    @staticmethod
    def build_forests(base_dir: str, physical_dir: str, logical_dir : str, flag : str, timeout : int) -> List['ProofForest']:
        sanitize = lambda s: re.sub(r'\s+', ' ', s.strip())
        defn_name = lambda n: n.split(':')[0].strip()
        is_bullet = lambda s: re.fullmatch(r'(-+|\++|\*+)', s) is not None

        result = []

        project_files = set(glob.glob(os.path.join(base_dir, '**/*.v'), recursive=True))
        for project_file in project_files:
            print('Processing %s...' % project_file)
            # this list populated below
            forest = []
            # create one proof forest for each project file
            result.append(ProofForest(project_file, forest))
            with ProofFile(project_file,
                           coq_lsp_options=('%s %s,%s' % (flag, physical_dir, logical_dir),),
                           timeout=timeout) as proof_file:

                ProofTree.print_errors(proof_file.errors)
                for _ in range(len(proof_file.steps)):
                    proof_file.exec()
                    ProofTree.print_errors(proof_file.errors)
                    if proof_file.in_proof:
                        goal_stack = []  # tracks current goals

                        # obtain theorem name
                        for name, dfn in proof_file.context.terms.items():
                            if dfn.file_path in project_files:
                                theorem_name = defn_name(name)

                        proof_tree = ProofTree(theorem_name)
                        forest.append(proof_tree)

                        while not proof_file.can_close_proof:
                            tactic = sanitize(proof_file.curr_step.text)
                            proof_file.exec()
                            # obtain current proof state by combining current goal and stack
                            current_state = []
                            # this is for the rare cases of open proofs with no goals! (first observed in cdf-mech-sem)
                            if proof_file.current_goals.goals is None:
                                break
                            for g in proof_file.current_goals.goals.goals:
                                local_context = tuple([sanitize(str(h)) for h in g.hyps])
                                locally_defined_symbols = tuple([defn_name(n) for h in g.hyps for n in h.names])
                                current_state.append((locally_defined_symbols, local_context, sanitize(g.ty)))
                            for stack in proof_file.current_goals.goals.stack:  # get remaining current goals from "Coq" stack and shelf
                                for g in stack[0] + stack[1]:
                                    local_context = tuple([sanitize(str(h)) for h in g.hyps])
                                    locally_defined_symbols = tuple([defn_name(n) for h in g.hyps for n in h.names])
                                    current_state.append((locally_defined_symbols, local_context, sanitize(g.ty)))
                            ################################ current proof state constructed
                            if is_bullet(tactic):  # ignore bullet tactics; current state won't change
                                continue

                            if goal_stack:
                                previous_goals = goal_stack.pop()
                                disappeared_goals = [g for g in previous_goals if g not in current_state]
                                new_goals = [g for g in current_state if g not in previous_goals]

                                for goal in disappeared_goals:
                                    proof_tree.__add_node(node=goal[2],
                                                          locally_defined_symbols=list(goal[0]),
                                                          local_context=list(goal[1]),
                                                          children=[g[2] for g in new_goals],
                                                          tactic=tactic)
                            goal_stack.append(current_state)
        return result


class ProofForest:
    def __init__(self,
                 file_path : str,
                 proof_trees : List[ProofTree]):
        self.__file_path = file_path
        self.__proof_trees = proof_trees

    def get_file_path(self) -> str:
        return self.__file_path

    def get_proof_trees(self) -> List[ProofTree]:
        return self.__proof_trees
