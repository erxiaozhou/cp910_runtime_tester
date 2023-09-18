import pytest
from generate_tcs_by_mutation_util.byte_seq_mask_mutator import _delete_op, _get_pos_outof_masks, _get_pos_outof_masks_insert, _in_masks, _insert_op
from generate_tcs_by_mutation_util.byte_seq_mask_mutator import _replace_op


masks1 = [[0, 11], [12, 15]]
masks2 = [[20, 21]]


@pytest.mark.parametrize('pos, masks', [[0, masks1], [10, masks1], [14, masks1], [20, masks2]])
def test_in_masks_True(pos, masks):
    assert _in_masks(pos, masks)


@pytest.mark.parametrize('pos, masks', [[11, masks1], [-1, masks1], [15, masks1], [19, masks2]])
def test_in_masks_False(pos, masks):
    assert not _in_masks(pos, masks)


# ============================== test ops ==============================
ba1 = bytearray([0, 1, 2])
replace_testing_paras = [
    [0, 10, ba1, bytearray([10, 1, 2])],
    [1, 255, ba1, bytearray([0, 255, 2])],
    [2, 0, ba1, bytearray([0, 1, 0])]
]


@pytest.mark.parametrize('pos, new_char, s, r', replace_testing_paras)
def test_replace_op(pos, new_char, s, r):
    assert r == _replace_op(pos, new_char, s)


insert_testing_paras = [
    [0, 10, ba1, bytearray([10, 0, 1, 2])],
    [1, 255, ba1, bytearray([0, 255, 1, 2])],
    [2, 0, ba1, bytearray([0, 1, 0, 2])],
    [3, 0, ba1, bytearray([0, 1, 2, 0])]
]


@pytest.mark.parametrize('pos, inserted_char, s, r', insert_testing_paras)
def test_insert_op(pos, inserted_char, s, r):
    assert r == _insert_op(pos, inserted_char, s)


delete_testing_paras = [
    [0, ba1, bytearray([1, 2])],
    [1, ba1, bytearray([0, 2])],
    [2, ba1, bytearray([0, 1])]
]


@pytest.mark.parametrize('pos, s, r', delete_testing_paras)
def test_delete_op(pos, s, r):
    assert r == _delete_op(pos, s)


# ============================== test get position ==============================
ba2 = bytearray(range(21))
masks3 = [[0, 5], [16, 21]]
r1 = [0] * 11 + [1] * 1 + [0] * 3 + [1] * 6
r2 = [1] * 20 + [0] * 1
r3 = [0] * 5 + [1] * 11 + [0] * 5
outof_masks_para = [
    [ba2, masks1, r1],
    [ba2, masks2, r2],
    [ba2, masks3, r3]
]


@pytest.mark.parametrize('s, masks, r', outof_masks_para)
def test_get_pos_outof_masks(s, masks, r):
    positions = set()
    for _ in range(1000):
        positions.add(_get_pos_outof_masks(s, masks))
    for i, val in enumerate(r):
        if val == 0:
            assert i not in positions, print(positions)
        else:
            assert val == 1
            assert i in positions


# 0000000000 0000000000 0
r1 = [1] * 1 + [0] * 10 + [1] * 2 + [0] * 2 + [1] * 7
r2 = [1] * 22
r3 = [1] * 1 + [0] * 4 + [1] * 12 + [0] * 4 + [1] * 1
outof_masks_para_insert = [
    [ba2, masks1, r1],
    [ba2, masks2, r2],
    [ba2, masks3, r3]
]


@pytest.mark.parametrize('s, masks, r', outof_masks_para_insert)
def test_get_pos_outof_masks_insert(s, masks, r):
    positions = set()
    for _ in range(1000):
        positions.add(_get_pos_outof_masks_insert(s, masks))
    for i, val in enumerate(r):
        if val == 0:
            assert i not in positions, print(positions)
        else:
            assert val == 1
            assert i in positions, print(positions)
