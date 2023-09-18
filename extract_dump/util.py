from pathlib import Path
from abc import abstractclassmethod
from .dump_data_util import dumpData
from path_group_util import cmnImplResultPathGroup


def is_failed_content(content):
    assert isinstance(content, str), print(content)
    content = content.lower()
    if 'error' in content:
        return True
    elif 'failed' in content:
        return True
    elif 'exception' in content:
        return True
    elif 'aborted' in content:
        return True
    elif 'aborting' in content:
        return True
    else:
        return False


class uninstResultInitializer(dumpData):
    def __init__(self, has_timeout, has_crash, features=None, log_content=None, name=None):
        super().__init__()
        self.has_timeout = has_timeout
        self.has_crash = has_crash
        self.log_content = log_content
        self.features = features.copy()
        self.name = name
        self.common_initialize()

    def common_initialize(self):
        self._init_has_failed_content()
        self._init_failed_exec()
        self._init_can_initialize()

    def _init_failed_exec(self):
        self.failed_exec = self.log_has_failed_content or self.has_timeout or self.has_crash

    def _init_has_failed_content(self):
        self.log_has_failed_content = is_failed_content(self.log_content)

    def _init_can_initialize(self):
        self.can_initialize = True

class halfDumpResultInitializer(uninstResultInitializer):
    def __init__(self, paths, has_timeout, has_crash, features=None, log_content=None, name=None):
        self.paths = paths
        super().__init__(has_timeout, has_crash, features, log_content, name)
        assert isinstance(paths, cmnImplResultPathGroup)
        if Path(self.vstack_path).exists():
            self._init_stack(self.vstack_path)

    @abstractclassmethod
    def _init_stack(self, *args, **kwargs): pass

    def common_initialize(self):
        self._init_has_failed_content()
        self._init_failed_exec()
        self._init_can_initialize()
        self._init_has_instance()

    def _init_can_initialize(self):
        self.can_initialize = Path(self.vstack_path).exists()

    def _init_has_instance(self):
        self.has_instance = _has_instance(self.has_instance_path)

    @property
    def to_dict(self):
        new_data = dumpData()
        for k in new_data.__dict__.keys():
            new_data.__dict__[k] = self.__dict__[k]
        return new_data.to_dict

    @property
    def vstack_path(self):
        return self.paths.vstack_path

    @property
    def has_instance_path(self):
        return self.paths.inst_path

class fullDumpResultInitializer(halfDumpResultInitializer):
    def __init__(self, paths, has_timeout, has_crash, features=None, log_content=None, name=None):
        super().__init__(paths, has_timeout, has_crash, features, log_content, name)
        if Path(self.store_path).exists():
            self._init_store(self.store_path)

    @abstractclassmethod
    def _init_store(self, *args, **kwargs): pass

    def _init_can_initialize(self):
        self.can_initialize = Path(self.store_path).exists() and Path(self.vstack_path).exists()

    @property
    def store_path(self):
        return self.paths.store_path

def _has_instance(path):
    has_instance_ = False
    path = Path(path)
    if path.exists():
        with open(path,'rb') as f:
            content = f.read()
        assert bytearray(content) == bytearray([0xff, 0xff, 0xff, 0xff]), print(content)
        has_instance_ = True
    else:
        pass
    return has_instance_
