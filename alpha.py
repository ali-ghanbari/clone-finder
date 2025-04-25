def find_alpha_equiv_goals(proj_logical_path, min_proof_sz, goal_ast_map, goals_list):
    with open('alpha-%s-%d.txt' % (proj_logical_path, min_proof_sz), mode='w') as results_file:
        for i in range(len(goals_list)):
            goal_1 = goals_list[i][0]
            thm_name_1 = goals_list[i][1]
            file_name_1 = goals_list[i][2]
            proof_1 = goals_list[i][3]
            goal_1_gen = goals_list[i][4]
            a1 = goal_ast_map[goal_1_gen]
            for j in range(i + 1, len(goals_list)):
                goal_2 = goals_list[j][0]
                thm_name_2 = goals_list[j][1]
                if thm_name_1 == thm_name_2:
                    continue
                file_name_2 = goals_list[j][2]
                proof_2 = goals_list[j][3]
                goal_2_gen = goals_list[j][4]
                a2 = goal_ast_map[goal_2_gen]
                if a1.alpha_equiv(a2):
                    results_file.write('Goal 1: %s\n' % goal_1)
                    results_file.write('\t Inside theorem: %s\n' % thm_name_1)
                    results_file.write('\t Inside file: %s\n' % file_name_1)
                    results_file.write('\t Proof:\n')
                    results_file.write('\n'.join(map(lambda x: '\t\t' + x, proof_1)))
                    results_file.write('\nGoal 2: %s\n' % goal_2)
                    results_file.write('\t Inside theorem: %s\n' % thm_name_2)
                    results_file.write('\t Inside file: %s\n' % file_name_2)
                    results_file.write('\t Proof:\n')
                    results_file.write('\n'.join(map(lambda x: '\t\t' + x, proof_2)))
                    results_file.write('\n')
                    results_file.write('=' * 50)
                    results_file.write('\n')
