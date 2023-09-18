from file_util import byte2str
import subprocess
from pathlib import Path


def combine_path(p1, p2):
    s = Path(p1) / p2
    return str(s)


def exec_impl_and_collect_log(cmd_fmt, timeout_th, wasm_path, err_channel):
    assert err_channel in ['stdout', 'stderr', 'stdout_stderr']
    has_timeout = False
    has_crash = False
    cmd = cmd_fmt.format(wasm_path)
    try:
        p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, timeout=timeout_th)

        if err_channel == 'stdout_stderr':
            content = byte2str(p.stdout).strip(' \t\n')
            err_byte_content = byte2str(p.stderr).strip(' \t\n')
            if len(err_byte_content):
                content = content + '\n' + err_byte_content
        elif err_channel == 'stdout':
            content = byte2str(p.stdout).strip(' \t\n')
        elif err_channel == 'stderr':
            content = byte2str(p.stderr).strip(' \t\n')
        # detect crash
        if err_channel == 'stderr':
            has_crash = detect_has_crash_in_err(content)
        else:
            err_output = byte2str(p.stderr).strip(' \t\n')
            has_crash = (len(err_output) > 0)
    except subprocess.TimeoutExpired:
        has_timeout = True
        content = ''

    return has_timeout, has_crash, content

def detect_has_crash_in_err(log):
    if 'Segmentation fault (core dumped)' in log:
        return True
    return False
