from extract_dump import are_different
from load_results_util import load_results_from_one_dumped_data_dir
from file_util import read_json, save_json, check_dir
from pathlib import Path
from functools import lru_cache
from tqdm import tqdm


def dumped_data_base_dir2reason_summary_json(result_json_path, dumped_data_base_dir, except_log, considered_keys=None):
    reason_summary = {}
    except_tc_names = []
    for dumped_data_dir in tqdm(Path(dumped_data_base_dir).iterdir(), desc='In dumped_data_base_dir2reason_summary_json'):
        tc_name = dumped_data_dir.name
        try:
            dumped_results = load_results_from_one_dumped_data_dir(dumped_data_dir)
            difference_reason = are_different(dumped_results)
            if difference_reason:
                reason_key = _get_key_from_reason_content(difference_reason, considered_keys)
                if reason_key not in reason_summary:
                    reason_summary[reason_key] = []
                reason_summary[reason_key].append(tc_name)
        except Exception:
            except_tc_names.append(tc_name)
    save_json(result_json_path, reason_summary)
    save_json(except_log, except_tc_names)


def dumped_data_base_dir2reason_base_dir(dumped_data_base_dir, reason_base_dir):
    reason_base_dir = check_dir(reason_base_dir)
    dumped_data_base_dir = Path(dumped_data_base_dir)
    for tc_dumped_data_dir in tqdm(dumped_data_base_dir.iterdir(), desc='In dumped_data_base_dir2reason_base_dir'):
        tc_name = tc_dumped_data_dir.name

        dumped_results = load_results_from_one_dumped_data_dir(tc_dumped_data_dir)
        difference_reason = are_different(dumped_results)
        if difference_reason:
            save_json(reason_base_dir / f'{tc_name}.json', difference_reason)


def reason_base_dir2reason_summary_json(reason_base_dir, save_path, considered_keys=None):
    reason_summary = reason_base_dir2reason_summary(reason_base_dir, considered_keys)
    save_json(save_path, reason_summary)


def reason_base_dir2reason_summary(reason_base_dir, considered_keys):
    reason_summary = {}
    dir_path = Path(reason_base_dir)
    for p in tqdm(dir_path.iterdir(), desc='In reason_base_dir2reason_summary'):
        tc_name = p.stem
        reason_key = _get_key_from_diff_result_p(p, considered_keys)
        if reason_key not in reason_summary:
            reason_summary[reason_key] = []
        reason_summary[reason_key].append(tc_name)
    return reason_summary


def _get_key_from_diff_result_p(p, considered_keys):
    content = read_json(p)
    sorted_tuple_str = _get_key_from_reason_content(content, considered_keys)
    return sorted_tuple_str


def _get_key_from_reason_content(content, considered_keys):
    assert isinstance(content, dict)
    return _get_key_from_reason_content_repr(repr(content), repr(considered_keys))


@lru_cache(maxsize=4096 * 4, typed=False)
def _get_key_from_reason_content_repr(content_repr, considered_keys_repr):
    considered_keys = eval(considered_keys_repr)
    content = eval(content_repr)
    sorted_list = []
    for k, v in content.items():
        if considered_keys is not None:
            v = [x for x in v if x in considered_keys]
        impl_repr = (k, tuple(sorted(v)))
        if len(v)> 0:
            sorted_list.append(impl_repr)
    sorted_list = sorted(sorted_list, key= lambda x : x[0])
    sorted_tuple_str = repr(tuple(sorted_list))
    return sorted_tuple_str
