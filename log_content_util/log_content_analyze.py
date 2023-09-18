import re
from pathlib import Path
from tqdm import tqdm
from file_util import check_dir, read_json, save_json
from .get_key_util import group_tc_names_by_log_key
from .get_key_util import supported_modes


def log_content_categorize_by_one_reason_path(reason_json_path, dumped_data_base_dir, log_categorize_dir, strategy_mode):
    assert strategy_mode in supported_modes
    reason2tc_result_dirs = get_reason2result_dirs_from_reason_json(reason_json_path, dumped_data_base_dir)
    assert isinstance(reason2tc_result_dirs, dict)
    log_categorize_dir = check_dir(log_categorize_dir)
    path2reason_content_pair = {}

    sigs = set()
    for file_idx, (reason_key, tc_result_dirs) in enumerate(reason2tc_result_dirs.items(), start=1):
        content_key2tc_names = group_tc_names_by_log_key(tc_result_dirs, strategy_mode, reason_key)
        assert isinstance(content_key2tc_names, dict)
        content_key2tc_names_path = str(log_categorize_dir / f'{file_idx}.json')
        save_json(content_key2tc_names_path, content_key2tc_names)

        for log_key in tqdm(content_key2tc_names.keys(), total=len(content_key2tc_names)):
            cleaned_reason_key = clean_reason_key(reason_key)
            inv_key = f'{content_key2tc_names_path}<-->{cleaned_reason_key}'
            path2reason_content_pair.setdefault(inv_key, []).append(log_key)
            sigs.add(log_key)

    save_json(log_categorize_dir / '0_reason_content_pair_inv_log.json', path2reason_content_pair)
    save_json(log_categorize_dir / '0_sigs.json', list(sigs))


def clean_reason_key(reason_key):
    return re.sub(r'[\'"]', '', reason_key)


def get_reason2result_dirs_from_reason_json(reason_json_path, result_base_dir):
    result_base_dir = Path(result_base_dir)
    reason2tc_result_dirs = {}
    reason_tc_names = read_json(reason_json_path)
    num = len(reason_tc_names)
    for k, v in tqdm(reason_tc_names.items(),total=num):
        reason2tc_result_dirs[k] = [result_base_dir/name for name in v]
    return reason2tc_result_dirs
