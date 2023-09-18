from functools import lru_cache
import re

def log_dict2key(dict_data_repr):
    key = _get_key_from_log_dict_repr(dict_data_repr)
    key = re.sub(r'[\'"]', '', key)
    return key


@lru_cache(maxsize=4096 * 4, typed=False)
def _get_key_from_log_dict_repr(processed_log_dict_repr):
    processed_log_dict = eval(processed_log_dict_repr)
    sorted_keys = get_sorted_keys(tuple(processed_log_dict.keys()))
    sorted_list = []
    for k in sorted_keys:
        impl_repr = (k, processed_log_dict[k])
        sorted_list.append(impl_repr)
    key = repr(tuple(sorted_list))
    return key


@lru_cache(maxsize=1024, typed=False)
def get_sorted_keys(keys):
    return sorted(keys, key=lambda x: x)