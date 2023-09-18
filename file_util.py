import os
import json
import struct
import subprocess
import time
from pathlib import Path
import pickle
import chardet
import logging


def pickle_dump(path, data):
    if isinstance(path, str):
        path = Path(path)
    with path.open("wb") as f:
        pickle.dump(data, f)


def pickle_load(path):
    if isinstance(path, str):
        path = Path(path)
    with path.open("rb") as f:
        data = pickle.load(f)
    return data


def check_dir(path, mkdir=True):
    if not isinstance(path, Path):
        path = Path(path)
    if mkdir:
        parent_path = path.parent
        if not parent_path.exists():
            check_dir(parent_path)
        if not path.exists():
            path.mkdir()
        return path
    return path.exists()


def read_json(path):
    if isinstance(path, str):
        path = Path(path)
    f = path.open(encoding="utf8")
    data = json.load(f)
    f.close()
    return data


def save_json(path, data):
    if isinstance(path, str):
        path = Path(path)
    f = path.open("w", encoding="utf8")
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()


def write_bytes(path, byte_seq):
    with open(path, 'wb') as fwriter:
        fwriter.write(byte_seq)


def read_bytes(path):
    with open(path, 'rb') as f:
        return bytearray(f.read())


def path_write(path, content):
    if isinstance(path, str):
        path = Path(path)
    with path.open('w', encoding='utf8') as f:
        f.write(content)


def rm_dir(dir):
    os.system("rm -rf {}".format(dir))
    return dir


def cp_file(src_path, tgt_path):
    os.system("cp {} {}".format(src_path, tgt_path))


def get_time_string():
    return time.strftime('%m-%d-%H-%M-%S', time.localtime())


def remove_file_without_exception(path):
    path = str(path)
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def print_ba(ba):
    ba = bytearray(ba)
    print([hex(x) for x in ba])


def bytes2uint(bs):
    int_val = int.from_bytes(bs, byteorder='little', signed=False)
    return int_val


def dir_file_num(path):
    cmd = 'ls {} | wc -l'.format(path)
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out_content = p.stdout.read().decode().strip('\n')
    assert out_content.isdigit()
    return int(out_content)


def f322bytes(val):
    return struct.pack('<f', val)


def f642bytes(val):
    return struct.pack('<d', val)


def bytes2f32(bs):
    return struct.unpack('=f', bs)


def byte2str(bs):
    if len(bs) == 0:
        return ''
    result = chardet.detect(bs)
    encoding = result['encoding']
    if encoding is not None:
        try:
            s = bs.decode(encoding)
        except UnicodeDecodeError as e:
            s = str(bs)
    else:
        s = str(bs)
    return s


def get_logger(logger_name, log_file_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel('DEBUG')
    file = logging.FileHandler(log_file_name, mode='w', encoding='utf8')
    fmt = logging.Formatter(
        fmt="%(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s")
    file.setFormatter(fmt)
    logger.addHandler(file)
    return logger
