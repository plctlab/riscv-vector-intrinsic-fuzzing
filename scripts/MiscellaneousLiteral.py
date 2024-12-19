mis_literal_start0 = "void compute"
mis_literal_start1 = "Op(RIF::OperatorBase *op) {\n"

def include_literal(filename):
    return "#include\"" + filename + "\""

def create_temp_op(op_type, op_id, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  return ret