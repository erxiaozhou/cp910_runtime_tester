from collections import Counter
from pathlib import Path
from .extract_keyword_from_content_util import func_sec_size_mismatch, runtime_self_unsupport
from .load_log_from_one_tc_result_util import load_log_from_one_tc_result
from .load_log_from_one_tc_result_util import load_log_from_dumped_results
from .extract_keyword_from_content_util import fd_opcode, SIMD_unsupport, illegal_type, reference_unsupport
from .log_dict2key_util import log_dict2key
from .one_runtime_log_util import get_one_runtime_log, oneRuntimeLog
from abc import abstractclassmethod


supported_modes = ['all', 's1', 's2', 's3', 'only_interesting', 'only_highlight', None]


def group_tc_names_by_log_key(tc_result_dirs, strategy, reason_key=None):
    if reason_key is not None:
        reason_key = eval(reason_key)
        new_key = {}
        for k, v in reason_key:
            if v == ('CannotExecute',):
                continue
            new_key[k] = v
        reason_key = new_key
    runtime_logs2tc_names = {}
    for tc_result_dir in tc_result_dirs:
        tc_name = Path(tc_result_dir).name
        runtime_logs = get_runtime_logs_from_dir(tc_result_dir, strategy)
        runtime_logs2tc_names.setdefault(runtime_logs, []).append(tc_name)
    if strategy == 'only_highlight':
        tmp_log_key2tc_names = rewrite_dict(runtime_logs2tc_names)
        log_key2tc_names = {}
        for log_key, tc_names in tmp_log_key2tc_names.items():
            if reason_key is not None:
                log_key.update_processed_log_dict(reason_key)
            log_key = log_key.processed_key
            log_key2tc_names[log_key] = tc_names
    else:
        log_key2tc_names = {}
        for runtime_logs, tc_names in runtime_logs2tc_names.items():
            if reason_key is not None:
                runtime_logs.update_processed_log_dict(reason_key)
            log_key = runtime_logs.processed_key
            log_key2tc_names[log_key] = tc_names
    return log_key2tc_names


def get_runtime_logs_from_dir(tc_result_dir, strategy):
    strategy2class = {
        'all': rawRuntimeLogs,
        's1': s1RuntimeLogs,
        's2': s2RuntimeLogs,
        's3': s3RuntimeLogs,
        'only_interesting': onlyInterestingRuntimeLogs,
        'only_highlight': onlyHighlightRuntimeLogs
    }
    assert strategy in strategy2class
    return strategy2class[strategy].from_tc_result_dir(tc_result_dir, strategy)


class runtimeLogs:
    def __init__(self, log_dict, strategy=None) -> None:
        self.log_dict = log_dict
        self.strategy = strategy
        self._processed_log_dict = None
        self._has_processed = False

    def _get_processed_log_dict(self, strategy):
        assert not self._has_processed
        assert strategy in supported_modes
        processed_log_dict = self._process_log_dict(self.log_dict)
        self._has_processed = True
        return processed_log_dict

    @abstractclassmethod
    def _process_log_dict(self, log_dict):
        pass

    @property
    def get_key(self):
        if self._processed_log_dict is None:
            self._processed_log_dict = self._get_processed_log_dict(self.strategy)
        return repr(self._processed_log_dict)

    def update_processed_log_dict(self, new_processed_log_dict):
        if self._processed_log_dict is None:
            self._processed_log_dict = new_processed_log_dict.copy()
        else:
            self._processed_log_dict.update(new_processed_log_dict)

    @property
    def processed_key(self):
        return log_dict2key(self.get_key)

    def __hash__(self) -> int:
        return hash((self.get_key, self.strategy))

    def __eq__(self, o) -> bool:
        return self.get_key == o.get_key

    @classmethod
    def from_tc_result_dir(cls, tc_result_dir, strategy=None):
        return cls(load_log_from_one_tc_result(tc_result_dir), strategy)

    @classmethod
    def from_dumped_results(cls, dumped_results, strategy=None):
        return cls(load_log_from_dumped_results(dumped_results), strategy)

def _no_cross_process_log_dict(one_runtime_log_process_func, log_dict):
    processed_log_dict = {}
    for runtime_name, s in log_dict.items():
        one_runtime_log = get_one_runtime_log(s,runtime_name)
        processed_log = one_runtime_log_process_func(one_runtime_log)
        if processed_log:
            processed_log_dict[runtime_name] = processed_log
    return processed_log_dict


class filteredNormalRuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        processed_log_dict = {}
        for runtime_name, s in log_dict.items():
            one_runtime_log = get_one_runtime_log(s,runtime_name)
            processed_log = one_runtime_log.filter_normal
            if processed_log:
                processed_log_dict[runtime_name] = processed_log
        return processed_log_dict

class rawRuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        return _no_cross_process_log_dict(oneRuntimeLog.keyword_part, log_dict)

class s1RuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        return _no_cross_process_log_dict(oneRuntimeLog.summary_key_s1, log_dict)

class s2RuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        return _no_cross_process_log_dict(oneRuntimeLog.summary_key_s2, log_dict)

class s3RuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        return _no_cross_process_log_dict(oneRuntimeLog.summary_key_s3, log_dict)


class onlyInterestingRuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        processed_log_dict = _no_cross_process_log_dict(oneRuntimeLog.summary_key_s3, log_dict)
        vals = list(processed_log_dict.values())
        if 0 < vals.count(func_sec_size_mismatch) < len(vals):
            for runtime_name in processed_log_dict.keys():
                processed_log_dict[runtime_name] = func_sec_size_mismatch
        runtime_names = list(processed_log_dict.keys())
        # fd =======================================================
        has_fd = False
        # rule1: fd_opcode
        for v in processed_log_dict.values():
            if v == fd_opcode:
                has_fd = True
        # rule2: SIMD_unsupport
        if not has_fd:
            for processed_log in processed_log_dict.values():
                if processed_log == SIMD_unsupport:
                    has_fd = True
        # rule3: special runtimes
        if not has_fd:
            for runtime_name in ['iwasm_classic_interp_dump', 'iwasm_fast_interp_dump', 'iwasm_multi_jit_dump']:
                if processed_log_dict.get(runtime_name) == fd_opcode:
                    has_fd = True
        if has_fd:
            for runtime_name in runtime_names:
                if processed_log_dict[runtime_name] == illegal_type:
                    processed_log_dict[runtime_name] = runtime_self_unsupport
            for runtime_name in ['wasm3_dump', 'wasmi_interp', 'iwasm_classic_interp_dump', 'iwasm_fast_interp_dump']:
                if processed_log_dict.get(runtime_name) == fd_opcode:
                    processed_log_dict[runtime_name] = runtime_self_unsupport
        # ref =======================================================
        has_ref = False
        for processed_log in processed_log_dict.values():
            if processed_log == reference_unsupport:
                has_ref = True
                break
        if has_ref:
            for runtime_name in runtime_names:
                if processed_log_dict[runtime_name] == illegal_type:
                    processed_log_dict[runtime_name] = runtime_self_unsupport

        # some features are not supported by some runtimes, which is as expected
        for runtime_name in runtime_names:
            if processed_log_dict[runtime_name] == runtime_self_unsupport:
                processed_log_dict.pop(runtime_name)
        return processed_log_dict

class onlyHighlightRuntimeLogs(onlyInterestingRuntimeLogs):
    pass

def rewrite_dict(log_key2tc_names, aggressive=False):
    log_key2log_key_freq = {}

    log_kwds = set()
    for log_key in log_key2tc_names.keys():
        cur_log_kwds = list(eval(log_key.get_key).values())
        log_kwds.update(cur_log_kwds)
        log_key2log_key_freq[log_key] = {kwd:v/len(cur_log_kwds) for kwd, v in Counter(cur_log_kwds).items()}

    to_save_log_keys = set()
    if '{}' in log_key2log_key_freq:
        to_save_log_keys.add('{}')
    for kwd in log_kwds:
        max_v = -1
        for log_key, c in log_key2log_key_freq.items():
            if c.get(kwd, -5) >= max_v:
                max_v = c[kwd]
        if aggressive and (max_v < 0.5):
            continue
        for log_key, c in log_key2log_key_freq.items():
            if c.get(kwd, -5) == max_v:
                to_save_log_keys.add(log_key)
    log_key2tc_names = {k:log_key2tc_names[k] for k in to_save_log_keys}
    return log_key2tc_names
