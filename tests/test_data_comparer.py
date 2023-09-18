import pytest
from load_results_util import load_results_from_one_dumped_data_dir
from extract_dump.analyze_exec_instant import _get_can_execute_num


paras = [
    ['./tests/f32.abs_100', 1, 7]
]


@pytest.mark.parametrize('tc_result_dir, num, result_num', paras)
def test_get_can_execute_num(tc_result_dir, num, result_num):
    results = load_results_from_one_dumped_data_dir(tc_result_dir)
    assert _get_can_execute_num(results) == num
    assert len(results) ==  result_num
