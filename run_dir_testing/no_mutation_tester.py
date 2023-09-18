from extract_dump import at_least_one_can_instantiate
from .tester_util import test_one_tc
from .tester_util import post_process_arrording_to_diff_reason
from .tester import Tester
from file_util import check_dir, cp_file
from file_util import get_logger
from .tester_util import testerExecInfo
from .tester_util import testerExecPaths
from tqdm import tqdm
logger = get_logger(__name__, 'tt/no_mutation_tester.log')

class noMutationTester(Tester):
    def __init__(self):
        pass

    def run_testing(self, exec_paths, impls, tc_paths_iterator):
        assert isinstance(exec_paths, testerExecPaths)
        para_paths = noMutationTestingPaths.from_testerExecPaths(exec_paths)
        exec_info = testing_without_mutation(para_paths, impls, tc_paths_iterator)
        return exec_info

    def __repr__(self):
        return self._common_brief_info()


def testing_without_mutation(exec_paths, impls, tc_paths_iterator):
    exec_info = testerExecInfo()
    for tc_name, tc_path in tqdm(tc_paths_iterator):
        try:
            exec_info.ori_tc_num += 1
            tc_dumped_data_dir = check_dir(exec_paths.dumped_data_base_dir / tc_name)
            dumped_results, difference_reason = test_one_tc(tc_dumped_data_dir, impls, tc_path)
            can_instantiate_ = at_least_one_can_instantiate(dumped_results)
            exec_info.all_exec_times += 1
            if can_instantiate_:
                exec_info.at_least_one_to_analyze += 1
            post_process_arrording_to_diff_reason(exec_paths, tc_dumped_data_dir, exec_info, tc_path, tc_name, difference_reason)
        except (RuntimeError, Exception) as e:
            logger.debug(f'tc_path: {tc_path}')
            logger.debug(f'error: {e}')
            cp_file(tc_path, exec_paths.except_dir)
    return exec_info


class noMutationTestingPaths:
    def __init__(self, dumped_data_base_dir, diff_tc_dir, reason_dir, except_dir):
        self.dumped_data_base_dir = dumped_data_base_dir
        self.diff_tc_dir = diff_tc_dir
        self.reason_dir = reason_dir
        self.except_dir = except_dir

    @classmethod
    def from_testerExecPaths(cls, tester_exec_paths):
        return cls(tester_exec_paths.dumped_data_base_dir, tester_exec_paths.diff_tc_dir, tester_exec_paths.reason_dir, tester_exec_paths.except_dir)
