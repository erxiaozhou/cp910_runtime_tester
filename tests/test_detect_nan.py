import pytest
from nan_detect_util import is_nan
from nan_detect_util import is_anan
from nan_detect_util import is_cnan
from nan_detect_util import is_illegal_anan
from nan_detect_util import process_f32_64
from file_util import f322bytes, f642bytes
from extract_dump.process_dump_data_util import get_f64, get_f32
import numpy as np


ba_vals = [
    bytearray(b'\x00\x00\x80\x7f'),  # inf
    bytearray(b'\x00\x00\x80\xff'),  # -inf
    bytearray(b'\x00\x00\xc0\x7f'),  # c nan
    bytearray(b'\x00\x00\xc0\xff'),  # -c nan
    bytearray(b'\x20\x00\xc0\x7f'),  # a nan
    bytearray(b'\x20\x00\xc0\xff'),  # -a nan
    bytearray(b'\x20\xff\xc0\x7f'),  # a nan
    bytearray(b'\x20\xff\xc0\xff'),  # -a nan
    bytearray(b'\x00\x00\x00\x00\x00\x00\xf0\x7f'),  # inf
    bytearray(b'\x00\x00\x00\x00\x00\x00\xf0\xff'),  # -inf
    bytearray(b'\x00\x00\x00\x00\x00\x00\xf8\x7f'),  # c nan
    bytearray(b'\x00\x00\x00\x00\x00\x00\xf8\xff'),  # -c nan
    bytearray(b'\x20\x00\xff\x00\x00\x00\xf8\x7f'),  # a nan
    bytearray(b'\x20\x00\xff\x00\x00\x00\xf8\xff'),  # -a nan
    bytearray(b'\x20\x00\x1c\x00\x00\x00\xf8\x7f'),  # a nan
    bytearray(b'\x20\x00\x1c\x00\x00\x00\xf8\xff'),  # -a nan
    bytearray(b'\x39\x00\x00\x00\x00\x00\xf0\x7f'),  # a inf?
    bytearray(b'\x39\x00\x00\x00\x00\x00\xf0\xff'),  # - a inf?
]


ba_vals_is_nan = [
    False,
    False,
    True,
    True,
    True,
    True,
    True,
    True,
    False,
    False,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True
]


ba_vals_is_anan = [
    False,
    False,
    False,
    False,
    True,
    True,
    True,
    True,
    False,
    False,
    False,
    False,
    True,
    True,
    True,
    True,
    False,
    False
]

ba_vals_is_cnan = [
    False,
    False,
    True,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    True,
    True,
    False,
    False,
    False,
    False,
    False,
    False
]


float_values = [
    0.0,
    1.0,
    1.0e-10,
    1.0e20,
    1.0e-20,
    -1,
    250.149,
    -119,
    np.inf,
    -np.inf
]


@pytest.mark.parametrize('ba, r', zip(ba_vals, ba_vals_is_nan))
def test_is_nan_on_ba(ba, r):
    assert is_nan(ba) == r


@pytest.mark.parametrize('ba, r', zip(ba_vals, ba_vals_is_anan))
def test_is_anan_on_ba(ba, r):
    assert is_anan(ba) == r


@pytest.mark.parametrize('ba, r', zip(ba_vals, ba_vals_is_cnan))
def test_is_cnan_on_ba(ba, r):
    assert is_cnan(ba) == r

@pytest.mark.parametrize('val', float_values)
def test_is_nan_on_common_floats(val):
    assert not is_nan(f322bytes(val))
    assert not is_nan(f642bytes(val))


@pytest.mark.parametrize('val', float_values)
def test_is_anan_on_common_floats(val):
    assert not is_anan(f322bytes(val))
    assert not is_anan(f642bytes(val))
    assert not is_cnan(f322bytes(val))
    assert not is_cnan(f642bytes(val))


@pytest.mark.parametrize('val', float_values)
def test_f32_transformation(val):
    ba = bytearray(f322bytes(val))
    ba2 = f322bytes(get_f32(ba))
    assert ba == ba2


@pytest.mark.parametrize('val', float_values)
def test_f64_transformation(val):
    ba = bytearray(f642bytes(val))
    ba2 = f642bytes(get_f64(ba))
    assert ba == ba2


@pytest.mark.parametrize('val', float_values)
def test_process_f32_64_on_common_floats(val):
    assert not is_nan(process_f32_64(f322bytes(val)))
    assert not is_nan(process_f32_64(f642bytes(val)))
    assert not is_anan(process_f32_64(f322bytes(val)))
    assert not is_anan(process_f32_64(f642bytes(val)))
    assert not is_cnan(process_f32_64(f322bytes(val)))
    assert not is_cnan(process_f32_64(f642bytes(val)))


@pytest.mark.parametrize('ba, r', zip(ba_vals, ba_vals_is_nan))
def test_process_f32_64_on_ba(ba, r):
    assert is_nan(process_f32_64(ba)) == r
    assert not is_anan(process_f32_64(ba))

@pytest.mark.parametrize('ba', ba_vals)
def test_detect_nan_ty(ba):
    s = 0
    if is_nan(ba):
        s += 1
    if is_anan(ba):
        s -= 1
    if is_cnan(ba):
        s -= 1
    if is_illegal_anan(ba):
        s -= 1
    assert s == 0
