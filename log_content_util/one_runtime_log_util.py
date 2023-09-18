
from .extract_keyword_from_content_util import extract_keyword_from_content, keyword_part2possible_common_reason, get_categorize_info_coarse_summary, get_categorize_info_fine_summary
from functools import lru_cache
from abc import abstractclassmethod
import re


def get_one_runtime_log(s, runtime_name):
    runtime_name2class = {
        'wasm3_dump': oneWasm3RuntimeLog,
        'WasmEdge_disableAOT_newer': oneWasmEdgeRuntimeLog,
        'wasmi_interp': oneWasmiRuntimeLog,
        'wasmer_default_dump': oneWasmerRuntimeLog,
        'WAVM_default': oneWAVMRuntimeLog,
        'iwasm_fast_interp_dump': oneIwasmRuntimeLog,
        'iwasm_classic_interp_dump': oneIwasmRuntimeLog,
        'iwasm_multi_jit_dump': oneIwasmRuntimeLog
    }
    assert runtime_name in runtime_name2class
    return runtime_name2class[runtime_name](s, runtime_name)


class oneRuntimeLog():
    def __init__(self, s, runtime_name=None) -> None:
        self.s = s
        self.runtime_name = runtime_name
        self.filter_normal = self._filter_normal_output(s)
        self.filter_normal = re.sub('\n', ' ', self.filter_normal)
        self.filter_normal = self.filter_normal.strip('\'"\n\\ ')
        self._keyword_part = None

    @abstractclassmethod
    def _filter_normal_output(self, s):
        pass


    def keyword_part(self):
        if self._keyword_part is None:
            self._keyword_part = extract_keyword_from_content(self.filter_normal)
        return self._keyword_part

    def summary_key_s1(self):
        return keyword_part2possible_common_reason(self.keyword_part())

    def summary_key_s2(self):
        return get_categorize_info_coarse_summary(self.keyword_part())

    def summary_key_s3(self):
        s = get_categorize_info_fine_summary(self.keyword_part())
        s = re.sub(r'\d{1,}', '<num>', s)
        return s

    def __hash__(self) -> int:
        return hash(self.s)

    def __eq__(self, o) -> bool:
        return self.s == o.s


hex_p = r'0[xX][0-9a-fA-F]+'
num_p = r'^[\-\+]?(?:(?:\d+)|(?:[\.\+\d]+e[\-\+]?\d+)|(?:\d+\.\d+)|(?:nan)|(?:inf))\n?$'
wasm_path_p = r' [^ ]+\.wasm'
offset_p = r'\(at offset (?:(?:\d+)|(?:0[xX][0-9a-fA-F]+))\)'
time_p = r'\[[\-0-9]+ [\.:0-9]+\]'

class oneWasmerRuntimeLog(oneRuntimeLog):
    @lru_cache(maxsize=4096, typed=False)
    def _filter_normal_output(self, s):
        s = re.sub(offset_p, '', s)
        s = re.sub(wasm_path_p, '', s)
        return s

class oneIwasmRuntimeLog(oneRuntimeLog):
    @lru_cache(maxsize=4096, typed=False)
    def _filter_normal_output(self, s):
        s = re.sub(r'^\n*$', '', s)
        p = r'^0x[a-f\d]+:i(?:(?:64)|(?:32))$'
        s = re.sub(p, '', s)
        p = r'^.*:f(?:(?:64)|(?:32))$'
        s = re.sub(p, '', s)
        p = r'^\d:ref\.func$'
        s = re.sub(p, '', s)
        p = r'^(?:(?:func)|(?:extern)):ref\.null$'
        s = re.sub(p, '', s)
        p = r'^<0x[a-f0-9]{16} 0x[a-f0-9]{16}>:v128$'
        s = re.sub(p, '', s)
        return s

class oneWasmiRuntimeLog(oneRuntimeLog):
    @lru_cache(maxsize=4096, typed=False)
    def _filter_normal_output(self, s):
        s = re.sub(offset_p, '', s)
        s = re.sub(wasm_path_p, '', s)
        return s


class oneWAVMRuntimeLog(oneRuntimeLog):
    @lru_cache(maxsize=4096, typed=False)
    def _filter_normal_output(self, s):
        return s


class oneWasmEdgeRuntimeLog(oneRuntimeLog):
    @lru_cache(maxsize=4096, typed=False)
    def _filter_normal_output(self, s):
        s = re.sub(time_p, '', s)
        s = re.sub(wasm_path_p, '', s)
        p = r'Bytecode offset: 0[xX][0-9a-fA-F]+'
        s = re.sub(p, '', s)
        p = r' Code: 0[xX][0-9a-fA-F]+'
        s = re.sub(p, '', s)
        s = re.sub(num_p, '', s)
        return s


class oneWasm3RuntimeLog(oneRuntimeLog):
    @lru_cache(maxsize=4096, typed=False)
    def _filter_normal_output(self, s):
        p = r' *Result: *\-?[0-9\.]+$'
        s = re.sub(p, '', s)
        p = r' *Result: *\-?0[xX][0-9a-fA-F]+$'
        s = re.sub(p, '', s)
        p = r' *Result: *\-?(?:(?:nan)|(?:inf))'
        s = re.sub(p, '', s)
        if 'Empty Stack' in s:
            s = ''
        return s

@lru_cache(maxsize=4096 * 4, typed=False)
def filter_normal_output_common(s, runtime_name):
    one_runtime_log = get_one_runtime_log(s, runtime_name)
    s = one_runtime_log.filter_normal
    return s
