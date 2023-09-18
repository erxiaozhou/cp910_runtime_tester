import pytest
from debug_util import is_executable_by_impl


paras = [
    ['./tests/wasm_wats/f32.abs_1.wasm', True],
    ['./tests/wasm_wats/f32.abs_2.wasm', True],
    ['./tests/wasm_wats/f32.abs_100.wasm', False]
]

@pytest.mark.parametrize('path, r', paras)
def test_is_executable_by_log(path, r):
    assert is_executable_by_impl('wasmer_default_dump', path) == r
