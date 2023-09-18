import pytest
from generate_tcs_by_mutation_util.generate_tcs_by_mutation_util import _code_secion
from generate_tcs_by_mutation_util.generate_wasm_tc_util import prepare_template
from generate_tcs_by_mutation_util.get_mask_util.get_mask import get_byte_mask_range


paras = [
    ['./tests/wasm_wats/f32.abs_1.wasm', [[9, 47], [53, 69]]],
    ['./tests/wasm_wats/f32.abs_2.wasm', [[9, 47], [53, 69]]]
]


@pytest.mark.parametrize('tc_path, r', paras)
def test_get_byte_mask_range(tc_path, r):
    section_dict = prepare_template(tc_path)
    code_sec = bytearray(section_dict['code'])
    code_sec_info = _code_secion.from_code_sec_ba(code_sec)
    masks = get_byte_mask_range(code_sec_info.after_func1_length)
    assert masks == r
