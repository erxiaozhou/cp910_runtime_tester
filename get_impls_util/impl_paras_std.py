from extract_dump import iwasmFullClassicInterpDumpData
from extract_dump import wasmiFullDumpData
from extract_dump import wasm3FullDumpData
from extract_dump import wasmedgeFullDumpData
from extract_dump import wasmerFullDumpData
from extract_dump import iwasmFullFastInterpDumpData
from extract_dump import wavmFullDumpData
from pathlib import Path

runtimes_base_dir = '/home/zph/DGit/wasm_projects/std_runtime_test'
runtimes_base_dir = '/home/std_runtime_test'
runtimes_base_dir = Path(runtimes_base_dir)


impl_paras_std = {
    'wasmer_default_dump':{
        # Sep 27
        # release-3.0.0-beta.2
        # 6ca9a39c501ed6b0b8d7c793f9fba9a0d636b147
        'dump_dir': runtimes_base_dir / 'dump_wasmer_default',
        'standard_dir': runtimes_base_dir / 'ori_wasmer_default',
        'lastest_dir':runtimes_base_dir / 'ori_wasmer_lastest',
        'bin_relative_path': 'target/debug/wasmer',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} {} -i to_test',
        'lastest_cmd': '{} {} -i to_test',
        'err_channel': 'stderr',
        'dump_extractor': wasmerFullDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    },
    'wasmi_interp': {
        # Sep 24
        # v0.17.0
        # fc58331904c75afaac08e89238590a9bf6cd84d3
        'dump_dir': runtimes_base_dir / 'dump_wasmi',
        'standard_dir': runtimes_base_dir / 'ori_wasmi',
        'lastest_dir':runtimes_base_dir / 'ori_wasmi_lastest',
        'bin_relative_path': 'target/debug/wasmi_cli',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} {}  to_test',
        'lastest_cmd': '{} {}  to_test',
        'err_channel': 'stderr',
        'dump_extractor': wasmiFullDumpData,
        'support_multi_mem': False,
        'support_ref': False,
        'support_v128': False
    },
    'iwasm_classic_interp_dump':{
        # Sep 8
        # 6820af621265413b677e450cf126bb66c9f77077
        'dump_dir': runtimes_base_dir / 'dump_iwasm_interp_classic',
        'standard_dir': runtimes_base_dir / 'ori_iwasm_interp_classic',
        'lastest_dir':runtimes_base_dir / 'ori_iwasm_interp_classic_lastest',
        'bin_relative_path': 'product-mini/platforms/linux/build/iwasm',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} --heap-size=0 -f to_test {}',
        'lastest_cmd': '{} --heap-size=0 -f to_test {}',
        'err_channel': 'stdout',
        'dump_extractor': iwasmFullClassicInterpDumpData,
        'support_multi_mem': False,
        'support_ref': True,
        'support_v128': False
    },
    'iwasm_fast_interp_dump':{
        # Sep 8
        # 6820af621265413b677e450cf126bb66c9f77077
        'dump_dir': runtimes_base_dir / 'dump_iwasm_interp_fast',
        'standard_dir': runtimes_base_dir / 'ori_iwasm_interp_fast',
        'lastest_dir':runtimes_base_dir / 'ori_iwasm_interp_fast_lastest',
        'bin_relative_path': 'product-mini/platforms/linux/build/iwasm',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} --heap-size=0 -f to_test {}',
        'lastest_cmd': '{} --heap-size=0 -f to_test {}',
        'err_channel': 'stdout',
        'dump_extractor': iwasmFullFastInterpDumpData,
        'support_multi_mem': False,
        'support_ref': True,
        'support_v128': False
    },
    'wasm3_dump':{
        # Sep 14
        # fa18e9ece4dd45371deac69ded32838470a55c1b
        'dump_dir': runtimes_base_dir / 'dump_wasm3_default',
        'standard_dir': runtimes_base_dir / 'ori_wasm3_default',
        'lastest_dir':runtimes_base_dir / 'ori_wasm3_lastest',
        'bin_relative_path': 'build/wasm3',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} --func to_test {}',
        'lastest_cmd': '{} --func to_test {}',
        'err_channel': 'stderr',
        'dump_extractor': wasm3FullDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': False
    },
    'WasmEdge_disableAOT_newer':{
        # WasmEdge
        # Oct 8
        # 0.11.1
        # 980c52416bc53fafebcdf026cfc851a43dcb887c
        'dump_dir': runtimes_base_dir / 'dump_WasmEdge_disableAOT',
        'standard_dir': runtimes_base_dir / 'ori_WasmEdge_disableAOT',
        'lastest_dir':runtimes_base_dir / 'ori_WasmEdge_disableAOT_lastest',
        'bin_relative_path': 'build/tools/wasmedge/wasmedge',
        'dump_store_rpath' : 'dump_result/dump_store',
        'dump_vstack_rpath': 'dump_result/dump_vstack',
        'dump_instante_rpath': 'dump_result/dump_instantiation',
        'std_cmd': '{} --reactor {} to_test',
        'lastest_cmd': '{} --reactor {} to_test',
        'err_channel': 'stdout',
        'dump_extractor': wasmedgeFullDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    },
    'WAVM_default':{
        # May 14
        # 3f9a150cac7faf28eab357a2c5b83d2ec740c7d9
        'dump_dir': runtimes_base_dir / 'dump_WAVM_can_print',
        'standard_dir': runtimes_base_dir / 'ori_WAVM_can_print',
        'lastest_dir':runtimes_base_dir / 'ori_WAVM_can_print_lastest',
        'bin_relative_path': 'build/bin/wavm',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} run --function=to_test {}',
        'lastest_cmd': '{} run --function=to_test {}',
        'err_channel': 'stderr',
        'dump_extractor': wavmFullDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    }
}