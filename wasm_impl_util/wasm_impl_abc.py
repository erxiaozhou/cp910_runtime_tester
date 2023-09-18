from abc import ABC
from abc import abstractclassmethod


class WasmImpl(ABC):
    @abstractclassmethod
    def execute_and_collect(self):
        pass
