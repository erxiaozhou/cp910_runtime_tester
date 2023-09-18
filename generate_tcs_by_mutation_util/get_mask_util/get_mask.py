from file_util import read_bytes


local_set_nonv128_ba = read_bytes('./generate_tcs_by_mutation_util/get_mask_util/byte_mask/local_set_nonv128')
local_get_nonv128_ba = read_bytes('./generate_tcs_by_mutation_util/get_mask_util/byte_mask/local_get_nonv128')
local_set_v128_ba = read_bytes('./generate_tcs_by_mutation_util/get_mask_util/byte_mask/local_set_v128')
local_get_v128_ba = read_bytes('./generate_tcs_by_mutation_util/get_mask_util/byte_mask/local_get_v128')


def get_byte_mask_range(base):
    r = _get_mask_idx(base, [local_set_v128_ba, local_get_v128_ba])
    if len(r) == 0:
        r = _get_mask_idx(base, [local_set_nonv128_ba, local_get_nonv128_ba])
    assert len(r) in [0, 2]
    return r


def _get_mask_idx(base, masks):
    assert isinstance(base, bytearray)
    for m in masks:
        assert isinstance(m, bytearray)
    r = []
    for m in masks:
        start_idx = base.find(m)
        r_ = [start_idx, start_idx + len(m)]
        if r_[0] != -1:
            r.append(r_)
    return r
