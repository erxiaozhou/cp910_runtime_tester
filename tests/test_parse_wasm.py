from file_util import read_bytes
from generate_tcs_by_mutation_util.generate_wasm_tc_util import get_wasm_bytes_from_dict, prepare_template
import pytest


paras = [
    './tests/wasm_wats/f32.abs_1.wasm',
    './tests/wasm_wats/f32.abs_2.wasm'
]


@pytest.mark.parametrize('tc_path', paras)
def test_prepare_template(tc_path):
    ori_wasm_bytes = read_bytes(tc_path)
    section_dict = prepare_template(tc_path)
    repack_wasm_bytes = get_wasm_bytes_from_dict(section_dict)
    assert ori_wasm_bytes == repack_wasm_bytes
