from get_impls_util import get_std_impls
from run_dir_testing import test_and_analyze
from run_dir_testing import mutationParas


if __name__ == '__main__':
    tested_dir = '/home/spec/extract_document/generated_tcs/v19/tcs'
    result_base_dir = '/host_data/v19_no_mutation'
    impls = get_std_impls()
    paras = mutationParas.get_no_mutation_paras(result_base_dir, tested_dir, impls=impls)
    test_and_analyze(result_base_dir, paras, impls=impls)
