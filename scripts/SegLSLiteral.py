seg_load_literal_start0 = "void compute"
seg_load_literal_start1 = "Op(RIF::OperatorBase *op) {\n"

seg_load_literal_no_mask_body = '''

'''

seg_load_literal_no_mask_end = '''

'''

seg_load_literal_mask_body = '''

'''

seg_load_literal_mask_end = '''

'''


def include_literal(filename):
    return "\t#include\"" + filename + "\""

def create_seg_load_no_mask_op(op_type, op_id, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += seg_load_literal_start0 + op_type + seg_load_literal_start1
  print(output_nfield)
  for i in range(int(output_nfield)) :
    var = chr(ord('a') + i)
    ret += "  auto " + var + " = static_cast<RIF::" + input_types[0] + "Val *>(op->inputs[" + str(i) + "]); // scripts/SegLSLiteral.py create_seg_load_no_mask_op \n"
  ret += seg_load_literal_no_mask_body + include_literal("v" + op_id + ".h") + seg_load_literal_no_mask_end   
  return ret

def create_seg_load_mask_op(op_type, op_id, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += seg_load_literal_start0 + op_type + seg_load_literal_start1
  # mask
  ret += "  auto m = static_cast<RIF::OneDBoolVal *>(op->inputs[0]); // scripts/SegLSLiteral.py create_seg_load_mask_op\n"
  print(output_nfield)
  for i in range(int(output_nfield)) :
     var = chr(ord('a') + i)
     ret += "  auto " + var + " = static_cast<RIF::" + input_types[1] + "Val *>(op->inputs[" + str(i) + "]);  // scripts/SegLSLiteral.py create_seg_load_mask_op \n"
  ret += seg_load_literal_mask_body + include_literal("v" + op_id + ".h") + seg_load_literal_mask_end
  return ret