from concurrent import futures
from pathlib import Path
from extract_dump import dumpData
from path_group_util import cmnImplResultPathGroup


def exec_one_tc(impls, tc_path, tc_result_dir, tc_tgt_dump_dir):
    dumped_results = []
    for impl in impls:
        result = exec_one_runtime(impl, tc_result_dir, tc_path)
        assert isinstance(result, dumpData)
        dumped_results.append(result)
        dumped_path = _get_default_dumped_path(tc_tgt_dump_dir, result.name)
        result.dump(dumped_path)
    return dumped_results


def exec_one_tc_mth(impls, tc_path, tc_result_dir, tc_tgt_dump_dir):
    dumped_results = []
    to_do = []
    with futures.ProcessPoolExecutor(max_workers=len(impls)) as executor:
        for impl in impls:
            future = executor.submit(exec_one_runtime, impl,
                                     tc_result_dir, tc_path)
            to_do.append(future)
        for future in to_do:
            result = future.result()
            assert isinstance(result, dumpData)
            dumped_results.append(result)
            dumped_path = _get_default_dumped_path(tc_tgt_dump_dir, result.name)
            result.dump(dumped_path)
    return dumped_results


def exec_one_runtime(impl, tc_result_dir, tc_path):
    result_paths = cmnImplResultPathGroup.from_impl_name_and_tc_result_dir(impl.name, tc_result_dir)
    result = impl.execute_and_collect(tc_path, result_paths)
    return result


def _get_default_dumped_path(save_data_dir, impl_name):
    return Path(save_data_dir) / f'{impl_name}=dumped.pkl'
