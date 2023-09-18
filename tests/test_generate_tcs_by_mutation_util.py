from file_util import read_bytes
from generate_tcs_by_mutation_util.generate_tcs_by_mutation_util import _code_secion
from generate_tcs_by_mutation_util.generate_tcs_by_mutation_util import _generate_new_code_sec
from generate_tcs_by_mutation_util.generate_tcs_by_mutation_util import _get_new_func1_body
from generate_tcs_by_mutation_util.generate_tcs_by_mutation_util import _get_random_length
from generate_tcs_by_mutation_util.generate_wasm_tc_util import get_wasm_bytes_from_dict, prepare_template, read_next_leb_num
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


@pytest.mark.parametrize('tc_path', paras)
def test_code_section_from_code_sec_ba(tc_path):
    section_dict = prepare_template(tc_path)
    code_sec_bytes = section_dict['code']
    code_sec_info = _code_secion.from_code_sec_ba(code_sec_bytes)
    func_num, offset1 = read_next_leb_num(code_sec_bytes, offset=0)
    func1_size, offset2 = read_next_leb_num(code_sec_bytes, offset=offset1)
    assert func1_size == code_sec_info.func1_len
    assert len(code_sec_info.before_func) == offset1
    assert code_sec_info.before_func == bytearray([func_num])
    assert len(code_sec_info.func1_body) == func1_size
    content_after_func1 = code_sec_info.content_after_func1
    func1_body = code_sec_info.func1_body
    assert len(code_sec_bytes) == offset2 + len(func1_body) + len(content_after_func1)
    if len(content_after_func1):
        assert content_after_func1[-1] == 0xb


def test_code_section_from_code_sec_ba_fine1():
    tc_path = './tests/wasm_wats/f32.abs_1.wasm'
    section_dict = prepare_template(tc_path)
    code_sec_bytes = section_dict['code']
    assert len(code_sec_bytes) == 72
    code_sec_info = _code_secion.from_code_sec_ba(code_sec_bytes)
    func_num, offset1 = read_next_leb_num(code_sec_bytes, offset=0)
    func_size, offset2 = read_next_leb_num(code_sec_bytes, offset=offset1)
    assert offset1 == 1
    assert offset2 == 2
    assert code_sec_info.func1_len == func_size == 70
    assert code_sec_info.before_func == bytearray([1]) == bytearray([func_num])
    assert code_sec_info.func1_body[0] == 4
    assert code_sec_info.func1_body[-1] == 0xb
    assert code_sec_info.content_after_func1 == bytearray([])


def test_code_section_from_code_sec_ba_fine2():
    tc_path = './tests/wasm_wats/f32.abs_2.wasm'
    section_dict = prepare_template(tc_path)
    code_sec_bytes = section_dict['code']
    assert len(code_sec_bytes) == 92
    code_sec_info = _code_secion.from_code_sec_ba(code_sec_bytes)
    func_num, offset1 = read_next_leb_num(code_sec_bytes, offset=0)
    func_size, offset2 = read_next_leb_num(code_sec_bytes, offset=offset1)
    assert offset1 == 1
    assert offset2 == 2
    assert code_sec_info.func1_len == func_size == 70
    assert code_sec_info.before_func == bytearray([5]) == bytearray([func_num])
    assert code_sec_info.func1_body[0] == 4
    assert code_sec_info.func1_body[-1] == 0xb
    assert len(code_sec_info.content_after_func1) == 20
    assert code_sec_info.content_after_func1[0] == 4
    assert code_sec_info.content_after_func1[-1] == 0xb


@pytest.mark.parametrize('tc_path', paras)
def test_after_func1_length1(tc_path):
    section_dict = prepare_template(tc_path)
    code_sec_bytes = section_dict['code']
    code_sec_info = _code_secion.from_code_sec_ba(code_sec_bytes)
    func_num, offset1 = read_next_leb_num(code_sec_bytes, offset=0)
    func_size, offset2 = read_next_leb_num(code_sec_bytes, offset=offset1)
    part = code_sec_info.after_func1_length
    assert offset2 + len(part) == len(code_sec_bytes)
    assert code_sec_bytes[-len(part):] ==  part


@pytest.mark.parametrize('tc_path', paras)
def test_get_bytes_sec(tc_path):
    section_dict = prepare_template(tc_path)
    code_sec_bytes = section_dict['code']
    code_sec_info = _code_secion.from_code_sec_ba(code_sec_bytes)
    assert code_sec_bytes == code_sec_info.get_bytes()


test_random_length_paras = [10, 20, 30, 100]
@pytest.mark.parametrize('func1_length', test_random_length_paras)
def test_get_bytes(func1_length):
    lengths_expected = set([func1_length + i for i in [-1, 0, 1]])
    lengths_collected = set()
    for i in range(2000):
        lengths_collected.add(_get_random_length(func1_length))
    assert lengths_expected == lengths_collected


paras = [
    [bytearray(list(range(6))), [[0,2], [4,5]]],
    [bytearray(list(range(100))), [[6,20], [40,85]]],
    [bytearray(list(range(0,100))), []]
]


@pytest.mark.parametrize('bas, masks', paras)
def test_get_new_func1_body_cannot_mutate_input_bytes(bas, masks):
    ori_bas = bas[:]
    r = _get_new_func1_body(bas, masks)
    assert ori_bas is not bas
    assert ori_bas == bas


paras = [
    [read_bytes('./tests/wasm_wats/f32.abs_1.wasm'), [[10, 20], [30, 40]]],
    [read_bytes('./tests/wasm_wats/f32.abs_2.wasm'), [[0, 25], [30, 40]]]
]


@pytest.mark.parametrize('bas, masks', paras)
def test_generate_new_code_sec_cannot_mutate_input_bytes(bas, masks):
    ori_bas = bas[:]
    _generate_new_code_sec(bas, masks)
    assert ori_bas is not bas
    assert ori_bas == bas
