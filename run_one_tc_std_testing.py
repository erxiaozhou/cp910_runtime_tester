from pathlib import Path
from extract_dump import are_different
from exec_util import exec_one_tc_mth
from file_util import check_dir
from get_impls_util import get_std_impls
import os
import sys


def run_and_report_one_tc(tc_name, result_base_dir='result/one_tc_result'):
    impls = get_std_impls()
    assert Path(tc_name).exists()
    tc_path = tc_name
    tc_name = Path(tc_name).stem

    os.system('rm -rf {}'.format(result_base_dir))
    result_base_dir = check_dir(result_base_dir)
    tc_dumped_data_dir = check_dir(result_base_dir / tc_name)

    dumped_results = exec_one_tc_mth(impls, tc_path, tc_dumped_data_dir, tc_dumped_data_dir)
    difference_reason = are_different(dumped_results)

    diff_keys = []
    if difference_reason is not False:
        for r in difference_reason.values():
            diff_keys.extend(r)
        print(f'Difference: {difference_reason}')
    else:
        print('No difference')
    print('=' * 50)


if __name__ == '__main__':
    argv = sys.argv
    assert len(argv) == 2
    tc_path = argv[1]
    run_and_report_one_tc(tc_path)

