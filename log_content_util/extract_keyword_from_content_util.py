from functools import lru_cache

# runtime self unsupport
reference_unsupport = 'reference unsupport'
multi_memory_unsupport = 'multi memory'
too_many_local = 'too many local'
invalid_local_count = 'invalid local count'
stack_operand_overflow = 'stack operand overflow'
SIMD_unsupport = 'SIMD unsupport'

# section size related
section_mismatch = 'section mismatch'
unexpected_EOF = 'enexpected EOF'
func_sec_mismatch = 'func section size mismatch'
func_mismatch = 'function size mismatch'
# type related
illegal_type = 'illegal/unknown type'
illegal_local_type = 'invalid local type'
# memory related
## wrong alignment
large_alignment = 'large alignment'
illegal_alignment = 'illegal alignment'
memory_OOB = 'memory OOB'
export_memory_OOB = 'export memory OOB'
export_table_OOB = 'export table OOB'
# table related
table_OOB = 'table OOB'
elem_seg_oob = 'element segment OOB'
# function related
wasm3_stack_overflow = 'wasm3 stack overflow'
unknown_function = 'unknown function'
function_OOB = 'function OOB'
# zero byte expected
zero_byte_expected = 'zero byte expected'

# check and make it failed
type_mismatch = 'type mismatch'
illegal_int_encoding = 'illegal int encoding'
unreachable = 'unreachable'

fc_opcode = 'unsupported opcode fc'
fd_opcode = 'unsupported opcode fd'

control_structure_depth_related = 'control_structure_depth related'
illegal_opcode = 'illegal/unknown opcode'


categorize_info_coarse = {
    'memory index reserved byte must be zero': zero_byte_expected,
    'zero byte expected': zero_byte_expected,
    'operators remaining after end of function': func_sec_mismatch,
    'expected data but found end of stream': func_sec_mismatch,
    'unexpected end of section or function': func_sec_mismatch,
    'Invalid var_i32': illegal_int_encoding,
    'Invalid var_i64': illegal_int_encoding,
    'invalid var_u32': illegal_int_encoding,
    'integer too large': illegal_int_encoding,
    'integer representation too long': illegal_int_encoding,
    'Invalid unsigned LEB encoding': illegal_int_encoding,
    'Invalid signed LEB encoding': illegal_int_encoding,
    'invalid function code size': func_mismatch,
    'end of code reached before end of function': func_mismatch,
    'section size mismatch': section_mismatch,
    'section contained more data than expected': section_mismatch,
    'section overrun while parsing Wasm binary': section_mismatch,
    'control frames remain at end of function': section_mismatch,
    'section underrun while parsing Wasm binary': section_mismatch,
    'trailing bytes at end of section': section_mismatch,
    'table index out of bounds': table_OOB,
    'out of bounds table access': table_OOB,
    'outOfBoundsTableAccess': table_OOB,
    'unsupported opcode fc': fc_opcode,
    'unsupported opcode fd': fd_opcode,
    'Unknown 0xfd subopcode': fd_opcode,
    'SIMD support is not enabled': SIMD_unsupport,
    'v128 value type requires simd feature': SIMD_unsupport,
    'illegal opcode': illegal_opcode,
    'Unknown opcode': illegal_opcode,
    'unsupported opcode': illegal_opcode,
    'no compiler found for opcode': illegal_opcode,
    'no operation found for opcode': illegal_opcode,
    'invalid value type': illegal_type,
    'unknown value_type': illegal_type,
    'unknown value type': illegal_type,
    'malformed value type': illegal_type,
    'invalid local type':illegal_local_type,
    'multi-memory not enabled': multi_memory_unsupport,
    'bulk memory support is not enabled': multi_memory_unsupport,
    'multi-memory support is not enabled': multi_memory_unsupport,
    'memoryIndex must be less than module.memories.size': memory_OOB,
    'exportIt.index must be less than module.memories.size': export_memory_OOB,
    'exportIt.index must be less than module.tables.size': export_table_OOB,
    'reachedUnreachable': unreachable,
    'unreachable executed': unreachable,
    'Unknown 0xfc subopcode': fc_opcode,
    'out of bounds memory access': memory_OOB,
    'outOfBoundsMemoryAccess': memory_OOB,
    'type mismatch': type_mismatch,
    'non-typed select operands must have the same numeric type': type_mismatch,
    'unexpected end-of-file': unexpected_EOF,
    'Unexpected EOF': unexpected_EOF,
    'alignment must not be larger than natural': large_alignment,
    'alignment greater than natural alignment': large_alignment,
    'alignment too large': large_alignment,
    'Mismatched memory alignment': illegal_alignment,
    'Invalid alignment': illegal_alignment,
    'reference types support is not enabled': reference_unsupport,
    'locals exceed maximum': too_many_local,
    'local count too large': too_many_local,
    'too many locals': too_many_local,
    'invalid local count': invalid_local_count,
    'outOfBoundsElemSegmentAccess': elem_seg_oob,
    'elemSegmentIndex must be less than module.elemSegments.size()': elem_seg_oob,
    'compiling function overran its stack height limit': stack_operand_overflow,
    'wasm operand stack overflow': stack_operand_overflow,
    'fast interpreter offset overflow': stack_operand_overflow,
    'depth must be less than controlStack': control_structure_depth_related,
    'Expected non-empty control stack': control_structure_depth_related,
    'stack was not empty at end of control structure': control_structure_depth_related,
    '[trap] stack overflow': wasm3_stack_overflow,
    'functionIndex must be less than module.functions.size()': function_OOB,
    'function index out of bounds': function_OOB
}

runtime_self_unsupport = '<runtime self unsupport>'
func_sec_size_mismatch = '<function or section size mismatch>'
wrong_alignment = '<wrong alignment>'
illegal_type_ = '<illegal type or local type>'

categorize_info_fine = {
    reference_unsupport: runtime_self_unsupport,
    multi_memory_unsupport: runtime_self_unsupport, 
    SIMD_unsupport: runtime_self_unsupport, 
    too_many_local: runtime_self_unsupport, 
    stack_operand_overflow: runtime_self_unsupport,

    section_mismatch:func_sec_size_mismatch,
    unexpected_EOF:func_sec_size_mismatch,
    func_sec_mismatch:func_sec_size_mismatch,
    func_mismatch:func_sec_size_mismatch,

    large_alignment:wrong_alignment,
    illegal_alignment:wrong_alignment,

    illegal_type: illegal_type,
    illegal_local_type: illegal_type,
}


content_relation0_list = [
    'integer representation too long',
    'malformed reference type',
    'wasm operand stack overflow',
    'invalid var_u32',
    'compiling function overran its stack height limit',
    'v128 value type requires simd feature',
    'type mismatch',
    'trailing bytes at end of section',
    'integer too large',
    'Invalid signed LEB encoding',
    'unsupported opcode fd',
    'unsupported opcode fc',
    'Unknown opcode',
    'unknown memory',
    'unknown table',
    'bulk memory support is not enabled',
    'multi-memory support is not enabled',
    'memory index reserved byte must be zero',
    'SIMD support is not enabled',
    'table index out of bounds',
    'illegal opcode',
    'Unexpected EOF',
    'expected data but found end of stream',
    'Mismatched memory alignment',
    'alignment too large',
    'alignment greater than natural alignment',
    'elemSegmentIndex must be less than module.elemSegments.size()',
    'operators remaining after end of function',
    'Invalid alignment',
    'alignment must not be larger than natural',
    'unsupported opcode',
    'section size mismatch',
    'Expected non-empty control stack',
    'stack was not empty at end of control structure',
    'invalid lane index',
    'local index out of bounds',
    'reference types support is not enabled',
    'unexpected end-of-file',
    'Invalid var_i32',
    'Invalid var_i64',
    'zero byte expected',
    'out of bounds memory access',
    'outOfBoundsMemoryAccess',
    'Unknown 0xfc subopcode',
    'memoryIndex must be less than module.memories.size',
    'exportIt.index must be less than module.memories.size',
    'function index out of bounds',
    'invalid function type',
    'Unknown 0xfd subopcode',
    'invalid local type',
    'depth must be less than controlStack',
    'validation failed: unknown label',
    'out of bounds table access',
    'locals exceed maximum',
    'outOfBoundsElemSegmentAccess',
    'tail calls support is not enabled',
    'multi-memory not enabled',
    'outOfBoundsTableAccess',
    'outOfBoundsDataSegmentAccess',
    'Unknown 0xfe subopcode',
    'type index out of bounds',
    'section overrun while parsing Wasm binary',
    'control frames remain at end of function',
    'section underrun while parsing Wasm binary',
    'call stack exhausted',
    'invalid function code size',
    'branch depth too large',
    'no compiler found for opcode',
    'no operation found for opcode',
    'unknown value_type',
    'invalid value type',
    'Invalid type',
    'malformed value type',
    'invalid result arity',
    'unreachable',
    'non-typed select operands must have the same numeric type',
    'Invalid unsigned LEB encoding',
    'typed select must have exactly one result',
    'invalid local count',
    'undeclared function reference',
    'fast interpreter offset overflow',
    'unknown function',
    'functionIndex must be less than module.functions.size()',
    'unexpected end of section or function',
    'local count too large',
    'too many locals',
    'section contained more data than expected',
    'invalid reference type encoding',
    'end of code reached before end of function',
    '[trap] stack overflow'
]
content_relation0_list = sorted(content_relation0_list, key=lambda x: len(x), reverse=True)


content_relation2 = {
    'unsupported opcode fd': '<common reason>',
    'unsupported opcode fc': '<common reason>',
    'bulk memory support is not enabled': '<common reason>',
    'multi-memory support is not enabled': '<common reason>',
    'SIMD support is not enabled': '<common reason>',
    'reference types support is not enabled': '<common reason>',
    'Unknown 0xfc subopcode': '<common reason>',
    'Unknown 0xfd subopcode': '<common reason>',
    'wasm operand stack overflow': '<common reason>',
    'Validation error: locals exceed maximum': '<common reason>',
    'wasm operand stack overflow': '<common reason>',
    'compiling function overran its stack height limit': '<common reason>',
    'v128 value type requires simd feature': '<common reason>'
}


@lru_cache(maxsize=4096, typed=False)
def extract_keyword_from_content(content):
    for key in content_relation0_list:
        if key.lower() in content.lower():
            content = key
            break
    return content

@lru_cache(maxsize=4096, typed=False)
def keyword_part2possible_common_reason(keyword_part):
    keyword_part = keyword_part.lower()
    for k, v in content_relation2.items():
        if k.lower() in keyword_part:
            keyword_part = v
            break
    return keyword_part


@lru_cache(maxsize=4096, typed=False)
def get_categorize_info_coarse_summary(content):
    content = categorize_info_coarse.get(content, content)
    return content


@lru_cache(maxsize=4096, typed=False)
def get_categorize_info_fine_summary(content):
    content = get_categorize_info_coarse_summary(content)
    content = categorize_info_fine.get(content, content)
    return content

