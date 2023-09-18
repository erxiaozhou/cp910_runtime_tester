from run_one_tc_std_testing import run_and_report_one_tc
from pathlib import Path


for p in Path('./for_motivation_example').iterdir():
    assert p.suffix == '.wasm'
    print(f'Running {p} ...')
    run_and_report_one_tc(p)
