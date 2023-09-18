from .get_reason_util import reason_base_dir2reason_summary_json
from file_util import check_dir
from extract_dump.dump_data_util import no_exec_state_attrs


class reasonSummary:
    def __init__(self, reason_summary_base_dir, reason_base_dir, exec=True):
        reason_summary_base_dir = check_dir(reason_summary_base_dir)
        full_reason_summary_path = reason_summary_base_dir / 'full_summary.json'
        only_exec_reason_summary_path = reason_summary_base_dir / 'only_exec_summary.json'
        stack_reason_summary_path = reason_summary_base_dir / 'stack_summary.json'
        if exec:
            reason_base_dir2reason_summary_json(reason_base_dir, full_reason_summary_path)
            reason_base_dir2reason_summary_json(reason_base_dir, stack_reason_summary_path, no_exec_state_attrs)
            reason_base_dir2reason_summary_json(reason_base_dir, only_exec_reason_summary_path, ['CannotExecute', 'CanExecute', 'has_timeout', 'has_crash'])
        self.full_smry_path = full_reason_summary_path
        self.only_exec_smry_path = only_exec_reason_summary_path
        self.stack_smry_path = stack_reason_summary_path
