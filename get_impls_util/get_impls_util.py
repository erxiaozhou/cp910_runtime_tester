from wasm_impl_util import dumpRuntime
from wasm_impl_util import uninstRuntime
from .impl_paras_std import impl_paras_std


def get_std_impls():
    impls = []
    for name in impl_paras_std.keys():
        impl = dumpRuntime.from_dict(name, impl_paras_std[name])
        impls.append(impl)
    return impls


def get_std_uninst_impls(set_out2out_err=False):
    impls = []
    for name in impl_paras_std.keys():
        impl = uninstRuntime.from_std_dict(name, impl_paras_std[name], set_out2out_err=set_out2out_err)
        impls.append(impl)
    return impls
