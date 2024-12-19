mis_literal_start0 = "void compute"
mis_literal_start1 = "Op(RIF::OperatorBase *op) {\n"

mis_reinterpret_body_end = '''
  // scripts/MiscellaneousLiteral.py mis_reinterpret_body
  assert(a->length == out->length)
  auto length = a->length

  auto dataA = getRawPointer(a)
  auto dataOut = getRawPointer(out)

  for (int i = 0; i < length; ++i)
  {
    dataOut[i] = dataA[i]
  }
'''

def include_literal(filename):
    return "#include\"" + filename + "\""

def create_temp_op(op_type, op_id, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += mis_literal_start0 + op_type + mis_literal_start1

  return ret

def create_create_op(op_type, op_id, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += mis_literal_start0 + op_type + mis_literal_start1
  
  return ret

def create_get_op(op_type, op_id, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += mis_literal_start0 + op_type + mis_literal_start1
  
  return ret

def create_reinterpret_op(op_type, op_id, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += mis_literal_start0 + op_type + mis_literal_start1
  ret += "  auto a = static_cast<RIF::" + input_types[0] + "Val *>(op->inputs[0]); // scripts/MiscellaneousLiteral.py create_reinterpret_op \n"
  ret += "  auto out = static_cast<RIF::" + output_type[0] + "Val *>(op->outputs[0]); // scripts/MiscellaneousLiteral.py create_reinterpret_op \n"
  ret += mis_reinterpret_body_end
  return ret