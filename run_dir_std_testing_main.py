import sys
from run_dir_testing import test_and_analyze
from run_dir_testing import mutationParas
from get_impls_util import get_std_impls


if __name__ == '__main__':
    impls = get_std_impls()
    if len(sys.argv) == 3:
        tested_dir = sys.argv[1]
        result_base_dir = sys.argv[2]
    else:
        print('Use predefined paras.')
        tested_dir = '/home/extract_document/generated_tcs/v19/tcs'
        result_base_dir = '/home/v19_330'
    paras = mutationParas.get_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=30, mutate_num=3, mutate_prob=1, impls=impls)
    test_and_analyze(result_base_dir, paras, impls=impls)
