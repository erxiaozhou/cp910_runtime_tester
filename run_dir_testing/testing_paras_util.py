from pathlib import Path
from file_util import save_json
from time import time
from .tester import Tester
from .tester_util import testerExecInfo
from .tester_util import testerExecPaths
from .no_mutation_tester import noMutationTester
from .random_byte_mutation_tester import randomByteMutationTester


class testingInfoSaver:
    def __init__(self, paras):
        assert isinstance(paras, mutationParas)
        self.paras = paras
        self.start_time = None
        self.end_time = None

    def save_config(self, exec_info, config_path=None):
        assert isinstance(exec_info, testerExecInfo)
        if config_path is None:
            config_path = self.paras.tester_exec_paths.config_log_path
        d = {}
        d['config'] = self.paras.to_dict_for_save
        d['exec_info'] = exec_info.to_dict
        d['time'] = self.exec_time
        save_json(config_path, d)

    def init_start_time(self):
        self.start_time = time()

    def init_end_time(self):
        self.end_time = time()

    @property
    def exec_time(self):
        assert self.start_time is not None
        assert self.end_time is not None
        return self.end_time - self.start_time


class mutationParas:
    def __init__(self, tester, tester_exec_paths, tested_dir, impls) -> None:
        self.tester = tester
        assert isinstance(tester_exec_paths, testerExecPaths)
        self.tester_exec_paths = tester_exec_paths
        self.tested_dir = tested_dir
        self.impls = impls

    @classmethod
    def get_paras_with_mutation(cls, tested_dir, result_base_dir, impls, one_tc_limit=50, mutate_num=5, mutate_prob=1, tester_exec_paths=None):
        return cls(
            tested_dir=tested_dir,
            tester=randomByteMutationTester(one_tc_limit=one_tc_limit, mutate_num=mutate_num, mutate_prob=mutate_prob),
            impls=impls,
            tester_exec_paths=get_tester_exec_paths(result_base_dir, tester_exec_paths)
        )

    @classmethod
    def get_no_mutation_paras(cls, result_base_dir, tested_dir, impls, tester_exec_paths=None, check_not_exist=True):
        return cls(
            tested_dir=tested_dir,
            tester=noMutationTester(),
            impls=impls,
            tester_exec_paths=get_tester_exec_paths(result_base_dir, tester_exec_paths, check_not_exist)
        )

    @property
    def to_dict_for_save(self):
        d = {}
        for name, attr in self.__dict__.items():
            if isinstance(attr, Path):
                d[name] = str(attr)
            elif isinstance(attr, testerExecPaths):
                d[name] = attr.to_str_dict
            elif name == 'impls':
                impls = attr
                d['runtimes'] = [impl.name for impl in impls]
            elif isinstance(attr, Tester):
                d[name] = repr(attr)
            else:
                d[name] = attr
        return d


def get_tester_exec_paths(result_base_dir, tester_exec_paths=None, check_not_exist=True):
    if tester_exec_paths is None:
        tester_exec_paths = testerExecPaths.from_result_base_dir(result_base_dir, check_not_exist)
    return tester_exec_paths
