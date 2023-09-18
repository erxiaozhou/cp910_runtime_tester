import subprocess
from pathlib import Path


def exec_cmd(e_dir, e_ext):
    e_dir_txt = ','.join(e_dir)
    e_ext_txt = ','.join(e_ext)
    cmd = 'cloc --exclude-dir={} --exclude-ext={} .'.format(e_dir_txt, e_ext_txt)
    subprocess.run(cmd, shell=True)
    return cmd


exculde_dir = [
    'results',
    'tt',
    'run_one_tc_std_testing.py',
    'run_dir_std_testing_no_mutation_main.py',
    'run_dir_std_testing_main.py',
    'retrive_diff_num_from_reason_summary.py',
    'tests',
    'for_motivation_example',
    'script_run_motivation_example_test_cases.py',
    'script_cloc.py',
    'run_dir_std_testing_no_mutation_main.py',
]
exclude_ext = ['wasm', 'wat', 'json']

tmp_fnames = [f.name for f in Path('.').glob('tmp_*.py')]
script_fnames = [f.name for f in Path('.').glob('script*.py')]
expended_exclude_dir = exculde_dir + tmp_fnames + script_fnames
analyze_result_dir = ['analyze_reslut_util', 'log_content_util', 'stack_val_analyze']


def stat_framework_cloc():
    exec_cmd(expended_exclude_dir+analyze_result_dir, exclude_ext)


def stat_all_cloc():
    exec_cmd(expended_exclude_dir, exclude_ext)


if __name__ == '__main__':
    stat_framework_cloc()
    print('-----------------')
    stat_all_cloc()
