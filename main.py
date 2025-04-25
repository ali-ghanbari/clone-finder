import os
import pickle
import time
from argparse import ArgumentParser

from alpha import find_alpha_equiv_goals
from parsing.ast.goal_ast import Product
from parsing.goal_parser import GoalParser
from proof_tree import ProofTree
from util import is_prod_body, generalize


if __name__ == '__main__':
    parser = ArgumentParser(prog='clone-finder', description='Searches for goal clones in a Coq project')
    parser.add_argument('-b',
                        '--base-path',
                        dest='base_path',
                        help='Base path from where the .v files to be retrieved',
                        required=True)
    parser.add_argument('-p',
                        '--physical-path',
                        dest='physical_path',
                        help='Physical path to be mapped to the logical path',
                        required=True)
    parser.add_argument('-l',
                        '--logical-path',
                        dest='logical_path',
                        help='Logical path to be associated with the logical path',
                        required=True)
    parser.add_argument('-m',
                        '--path-mapping-option',
                        dest='path_mapping_option',
                        help='COQC path mapping option (default: Q)',
                        required=False,
                        default='Q')
    parser.add_argument('-s',
                        '--min-proof-size',
                        dest='min_proof_sz',
                        help='Minimum proof size (default: 5)',
                        required=False,
                        default='5')
    parser.add_argument('-to',
                        '--coq-lsp-timeout',
                        dest='coq_lsp_timeout',
                        help='Coq LSP client timeout (default: 500)',
                        required=False,
                        default='500')
    parser.add_argument('-t',
                        '--measure-time',
                        dest='measure_time',
                        help='Measure time (default: True)',
                        required=False,
                        default='True')
    args = parser.parse_args()

    proj_base_path = args.base_path
    if args.path_mapping_option not in {'R', 'Q'}:
        print('Error: unknown coqc path mapping option ' + args.path_mapping_option)
        quit()
    path_mapping_option = '-' + args.path_mapping_option
    proj_physical_path = args.physical_path
    proj_logical_path = args.logical_path
    min_proof_sz = int(args.min_proof_sz)
    coq_lsp_timeout = int(args.coq_lsp_timeout)
    if min_proof_sz < 1:
        print('Error: too small proof size (must be a positive integer)')
        quit()

    start_time = time.time()
    cache_file_name = 'forests-%s.pkl' % proj_logical_path
    if os.path.isfile(cache_file_name):
        print('Found cached Coq-LSP results. Loading...', end='', flush=True)
        forests = pickle.load(open(cache_file_name, 'rb'))
    else:
        forests = ProofTree.build_forests(proj_base_path,
                                          proj_physical_path,
                                          proj_logical_path,
                                          path_mapping_option,
                                          coq_lsp_timeout)

        print('Saving Coq-LSP results...', end='', flush=True)
        with open(cache_file_name, 'wb') as file:
            pickle.dump(forests, file)
    forests_construction_time = time.time() - start_time
    print(' [Done]')

    start_time = time.time()
    goals_list = None
    goal_ast_map = None
    goals_list_cache_file_name = 'goals-list-%s.pkl' % proj_logical_path
    goal_ast_map_cache_file_name = 'goal-ast-map-%s.pkl' % proj_logical_path
    if os.path.isfile(goals_list_cache_file_name) and os.path.isfile(goal_ast_map_cache_file_name):
        print('Found cached data. Loading...', end='', flush=True)
        goals_list = pickle.load(open(goals_list_cache_file_name, 'rb'))
        goal_ast_map = pickle.load(open(goal_ast_map_cache_file_name, 'rb'))
    else:
        print('Processing goals list...', end='', flush=True)
        goals_list = []
        goal_ast_map = dict()
        for forest in forests:
            proof_trees = forest.get_proof_trees()
            for i in range(len(proof_trees)):
                proof_tree = proof_trees[i]
                for n in proof_tree.get_nodes():
                    if len(proof_tree.get_proof(n)) >= min_proof_sz:
                        n_gen = generalize(proof_tree, n)
                        goal_ast_map[n_gen] = GoalParser(n_gen).parse()
                        goals_list.append((n,
                                           proof_tree.get_theorem_name(),
                                           forest.get_file_path(),
                                           proof_tree.get_proof(n),
                                           n_gen,
                                           proof_tree.get_local_context(n)))
        redundant_goals = set()
        for i in range(len(goals_list)):
            a1 = goal_ast_map[goals_list[i][4]]
            for j in range(len(goals_list)):
                a2 = goal_ast_map[goals_list[j][4]]
                if isinstance(a1, Product) and is_prod_body(a1, a2):
                    redundant_goals.add(goals_list[j][4])
        goals_list = [g for g in goals_list if g[4] not in redundant_goals]
        print(' [Done]')
        print('Saving goals list and goal AST map...', end='', flush=True)
        with open(goals_list_cache_file_name, 'wb') as file:
            pickle.dump(goals_list, file)
        with open(goal_ast_map_cache_file_name, 'wb') as file:
            pickle.dump(goal_ast_map, file)
    print(' [Done]')

    print('Finding clones...', end='')
    find_alpha_equiv_goals(proj_logical_path, min_proof_sz, goal_ast_map, goals_list)
    clone_finding_time = time.time() - start_time
    print(' [Done]')

    print('Proof forests construction time: %0.4f seconds' % forests_construction_time)
    print('Clone finding time: %.4f seconds' % clone_finding_time)
    print('Total time: %.4f seconds' % (clone_finding_time + forests_construction_time))
    if args.measure_time.lower() in ['true', 'True', 'yes', 'y']:
        with open('time-%s.txt' % proj_logical_path, 'w') as f:
            f.write('Proof forests construction time: %0.4f seconds\n' % forests_construction_time)
            f.write('Clone finding time: %.4f seconds\n' % clone_finding_time)
            f.write('Total time: %.4f seconds\n' % (clone_finding_time + forests_construction_time))
