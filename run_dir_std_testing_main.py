from run_dir_testing import test_and_analyze
from run_dir_testing import mutationParas
from get_impls_util import get_std_impls


if __name__ == '__main__':
    impls = get_std_impls()
    tested_dir = '/home/spec/extract_document/generated_tcs/v19/tcs'
    result_base_dir = '/host_data/v19_330_rerun_v2'
    paras = mutationParas.get_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=30, mutate_num=3, mutate_prob=1, impls=impls)
    test_and_analyze(result_base_dir, paras, impls=impls)
