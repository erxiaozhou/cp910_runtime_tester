from abc import abstractclassmethod


class Tester:
    @abstractclassmethod
    def run_testing(self):
        pass

    def _common_brief_info(self, **kwads):
        paras_parts = [f"<{k}:{v}>" for k, v in kwads.items()]
        paras_part = ' '.join(paras_parts)
        return f'{self.__class__.__name__} {paras_part}'
