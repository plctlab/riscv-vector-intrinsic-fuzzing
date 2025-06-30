vx_literal_start0 = "void compute"
vx_literal_start1 = "Op(RIF::OperatorBase *op) {\n"
vx_literal_nonmask_body = '''
  assert(a->length == c->length && b->length == 1);

  auto length = a->length;

  auto dataA = getRawPointer(a);
  auto dataB = getRawPointer(b);
  auto dataOut = getRawPointer(c);

  auto sew = op->typeInfo->sew.to_int();
  P.VU.vsew = sew;

  for (int i = 0; i < length; ++i) {
'''

vx_tu_literal_nonmask_body = '''
  assert(a->length == b->length && c->length == 1 && a->length == d->length);

  auto length = a->length;

  auto dataPassthru = getRawPointer(a);
  auto dataA = getRawPointer(b);
  auto dataB = getRawPointer(c);
  auto dataOut = getRawPointer(d);

  auto sew = op->typeInfo->sew.to_int();
  P.VU.vsew = sew;

  for (int i = 0; i < length; ++i) {
'''

vx_literal_nonmask_destructive_body = '''
  assert(a->length == c->length && a->length == d->length && b->length == 1);

  auto length = a->length;

  auto dataA = getRawPointer(a);
  auto dataB = getRawPointer(b);
  auto dataC = getRawPointer(c);
  auto dataOut = getRawPointer(d);

  auto sew = op->typeInfo->sew.to_int();

  #pragma push_macro("VI_VFP_VF_LOOP")
  #undef VI_VFP_VF_LOOP
  #define VI_VFP_VF_LOOP(BODY16, BODY32, BODY64)                               \\
  RIF::RawDatumOperand vd(dataA[i]);                                           \\
  RIF::RawDatumOperand rs1(*dataB);                                            \\
  RIF::RawDatumOperand vs2(dataC[i]);                                          \\
  switch (sew) {                                                               \\
  case e16:                                                                    \\
    BODY16;                                                                    \\
    break;                                                                     \\
  case e32:                                                                    \\
    BODY32;                                                                    \\
    break;                                                                     \\
  case e64:                                                                    \\
    BODY64;                                                                    \\
    break;                                                                     \\
  default:                                                                     \\
    assert(0);                                                                 \\
    break;                                                                     \\
  }                                                                            \\
  dataOut[i] = vd;

  #pragma push_macro("VI_VFP_VF_LOOP_WIDE")
  #undef VI_VFP_VF_LOOP_WIDE
  #define VI_VFP_VF_LOOP_WIDE(BODY16, BODY32)                                  \\
  RIF::RawDatumOperand vd(dataA[i]);                                           \\
  RIF::RawDatumOperand rs1(*dataB);                                            \\
  RIF::RawDatumOperand vs2(dataC[i]);                                          \\
  switch (sew) {                                                               \\
  case e16:                                                                    \\
    vs2 = f16_to_f32(vs2);                                                     \\
    rs1 = f16_to_f32(rs1);                                                     \\
    BODY16;                                                                    \\
    break;                                                                     \\
  case e32:                                                                    \\
    vs2 = f32_to_f64(vs2);                                                     \\
    rs1 = f32_to_f64(rs1);                                                     \\
    BODY32;                                                                    \\
    break;                                                                     \\
  default:                                                                     \\
    assert(0);                                                                 \\
    break;                                                                     \\
  }                                                                            \\
  dataOut[i] = vd;

  for (int i = 0; i < length; ++i) {
'''

vx_literal_nonmask_destructive_body_frm = '''
// script/VXLiteral.py vx_literal_nonmask_destructive_body_frm
  assert(a->length == d->length && b->length == 1);

  auto length = a->length;

  auto dataA = getRawPointer(a);
  auto dataB = getRawPointer(b);
  auto dataC = {}; //frm
  auto dataOut = getRawPointer(d);

  auto sew = op->typeInfo->sew.to_int();
  auto frm = dataC;
  P.VU.set_fround_mode(frm);
'''

vx_literal_nonmask_MulAddOperation_destructive_body_frm = '''
// script/VXLiteral.py vx_literal_nonmask_MulAddOperation_destructive_body_frm
  assert(a->length == c->length && a->length == e->length && b->length == 1);

  auto length = a->length;

  auto dataA = getRawPointer(a);
  auto dataB = getRawPointer(b);
  auto dataC = getRawPointer(c);
  auto dataD = {}; //frm
  auto dataOut = getRawPointer(e);

  auto sew = op->typeInfo->sew.to_int();
  auto frm = dataD;
  P.VU.set_fround_mode(frm);
'''

vx_literal_nonmask_widen_destructive_body_frm = '''
// script/VXLiteral.py vx_literal_widen_nonmask_destructive_body_frm
  assert(a->length == d->length && b->length == 1);

  auto length = a->length;

  auto dataA = getRawPointer(a); //vd
  auto dataB = getRawPointer(b); //vs2
  auto dataC = getRawPointer(c); //rs1
  auto dataD = {}; //frm
  auto dataOut = getRawPointer(e);

  auto sew = getVd(op)->typeInfo->sew.to_int();
  auto frm = dataD;
  P.VU.set_fround_mode(frm);
'''

vx_literal_nonmask_destructive_body_vxrm = '''
// script/VXLiteral.py vx_literal_nonmask_destructive_body_vxrm
  assert(a->length == c->length && a->length == e->length && b->length == 1);

  auto length = a->length;

  auto dataA = getRawPointer(a);
  auto dataB = getRawPointer(b);
  auto dataC = getRawPointer(c);
  auto dataD = {}; //vxrm
  auto dataOut = getRawPointer(e);

  auto sew = op->typeInfo->sew.to_int();
  auto vxrm = dataD;
  P.VU.set_vround_mode(vxrm);

'''

vx_literal_nonmask_destructive_macro_frm = '''
  #pragma push_macro("VI_VFP_VF_LOOP")
  #undef VI_VFP_VF_LOOP
  #define VI_VFP_VF_LOOP(BODY16, BODY32, BODY64)                               \\
  RIF::RawDatumOperand vd(dataA[i]);                                           \\
  RIF::RawDatumOperand rs1(*dataB);                                            \\
  RIF::RawDatumOperand vs2(dataC[i]);                                          \\
  switch (sew) {                                                               \\
  case e16:                                                                    \\
    BODY16;                                                                    \\
    break;                                                                     \\
  case e32:                                                                    \\
    BODY32;                                                                    \\
    break;                                                                     \\
  case e64:                                                                    \\
    BODY64;                                                                    \\
    break;                                                                     \\
  default:                                                                     \\
    assert(0);                                                                 \\
    break;                                                                     \\
  }                                                                            \\
  dataOut[i] = vd;

  #pragma push_macro("VI_VFP_VF_LOOP_WIDE")
  #undef VI_VFP_VF_LOOP_WIDE
  #define VI_VFP_VF_LOOP_WIDE(BODY16, BODY32)                                  \\
  RIF::RawDatumOperand vd(dataA[i]);                                           \\
  RIF::RawDatumOperand rs1(*dataB);                                            \\
  RIF::RawDatumOperand vs2(dataC[i]);                                          \\
  switch (sew) {                                                               \\
  case e16:                                                                    \\
    vs2 = f16_to_f32(vs2);                                                     \\
    rs1 = f16_to_f32(rs1);                                                     \\
    BODY16;                                                                    \\
    break;                                                                     \\
  case e32:                                                                    \\
    vs2 = f32_to_f64(vs2);                                                     \\
    rs1 = f32_to_f64(rs1);                                                     \\
    BODY32;                                                                    \\
    break;                                                                     \\
  default:                                                                     \\
    assert(0);                                                                 \\
    break;                                                                     \\
  }                                                                            \\
  dataOut[i] = vd;

'''

vx_literal_nonmask_end = '''
  }
}
'''

vx_ta_literal_nonmask_end = '''
  }
  for (int i = 0; i < length; ++i) {
    if (i & 1)
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
  }
}
'''

vx_tu_literal_nonmask_end = '''
  }
  for (int i = 0; i < length; ++i) {
    if (i & 1)
      dataOut[i] = dataPassthru[i];
  }
}
'''

vx_literal_nonmask_destructive_end = '''
  }
  #pragma pop_macro("VI_VFP_VF_LOOP")
  #pragma pop_macro("VI_VFP_VF_LOOP_WIDE")
}
'''

vx_tu_literal_nonmask_destructive_end = '''
  }
  #pragma pop_macro("VI_VFP_VF_LOOP")
  #pragma pop_macro("VI_VFP_VF_LOOP_WIDE")
  for (int i = 0; i < length; ++i) {
    if (i & 1) // tail element is undisturbed
      dataOut[i] = dataA[i];
  }
}
'''

vx_ta_literal_nonmask_destructive_end = '''
  }
  #pragma pop_macro("VI_VFP_VF_LOOP")
  #pragma pop_macro("VI_VFP_VF_LOOP_WIDE")
  for (int i = 0; i < length; ++i) {
    if (i & 1) // tail element is agnostic
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
  }
}
'''

vx_literal_mask_body = '''
  assert(a->length == b->length && a->length == d->length && c->length == 1);

  auto length = a->length;

  auto dataM = getRawPointer(a);
  auto dataA = getRawPointer(b);
  auto dataB = getRawPointer(c);
  auto dataOut = getRawPointer(d);

  auto sew = op->typeInfo->sew.to_int();
  P.VU.vsew = sew;

  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''

vx_literal_mask_vxrm_body = '''
  // script/VXLiteral.py vx_literal_mask_vxrm_body\n
  assert(a->length == b->length && c->length == 1 &&
         a->length == e->length);

  auto length = a->length;

  auto dataM = getRawPointer(a);  // mask
  auto dataA = getRawPointer(b);  // vs2
  auto dataB = getRawPointer(c);  //rs1
  auto dataC = {};  // vxrm
  auto dataOut = getRawPointer(e);

  auto vxrm = dataC;
  P.VU.set_vround_mode(vxrm);
  auto sew = op->typeInfo->sew.to_int();
  P.VU.vsew = sew;
'''

vx_literal_masked_frm_body = '''
  // script/VXLiteral.py vx_literal_mask_frm_body\n
  assert(a->length == b->length && c->length == 1 &&
         a->length == e->length);

  auto length = a->length;

  auto dataM = getRawPointer(a);  // mask
  auto dataA = getRawPointer(b);  // vs2
  auto dataB = getRawPointer(c);  //rs1
  auto dataC = {};  // frm
  auto dataOut = getRawPointer(e);

  auto frm = dataC;
  P.VU.set_fround_mode(frm);
  auto sew = op->typeInfo->sew.to_int();
  P.VU.vsew = sew;
'''

wf_literal_masked_frm_body = '''
  // script/VXLiteral.py wf_literal_mask_frm_body\n
  assert(c->length == 1 &&
         a->length == e->length);

  auto length = a->length;

  auto dataM = getRawPointer(a);  // mask
  auto dataA = getRawPointer(b);  // vs2
  auto dataB = getRawPointer(c);  //rs1
  auto dataC = {};  // frm
  auto dataOut = getRawPointer(e);

  auto frm = dataC;
  P.VU.set_fround_mode(frm);
  auto sew = op->typeInfo->sew.to_int();
  P.VU.vsew = sew;
'''

wf_literal_nonmasked_frm_body = '''
  // script/VXLiteral.py wf_literal_nonmasked_frm_body\n
  assert(a->length == d->length && c->length == 1);

  auto length = a->length;

  auto dataA = getRawPointer(a);  // vs2
  auto dataB = getRawPointer(b);  //rs1
  auto dataC = {};  // frm
  auto dataOut = getRawPointer(d);

  auto frm = dataC;
  P.VU.set_fround_mode(frm);
  auto sew = op->typeInfo->sew.to_int();
  P.VU.vsew = sew;
'''

mask_loop_start = '''
  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''


vx_literal_nonmask_vxrm_body = '''
  // script/VXLiteral.py vx_literal_nonmask_vxrm_body
  // vasub_vx
  assert(a->length == d->length && b->length == 1);

  auto length = a->length;

  auto dataA = getRawPointer(a);
  auto dataB = getRawPointer(b);
  auto dataC = {};  // c means vxrm
  auto dataOut = getRawPointer(d);

  auto vxrm = dataC;
  P.VU.set_vround_mode(vxrm);
  auto sew = op->typeInfo->sew.to_int();
  P.VU.vsew = sew;
'''

loop_start = '''
  for (int i = 0; i < length; ++i) {
'''

vx_literal_mask_destructive_body = '''
  assert(a->length == b->length && a->length == d->length &&
          a->length == e->length && c->length == 1);

  // script/VXLiteral.py vx_literal_mask_destructive_body
  auto length = a->length;

  auto dataM = getRawPointer(a);
  auto dataA = getRawPointer(b);
  auto dataB = getRawPointer(c);
  auto dataC = getRawPointer(d);
  auto dataOut = getRawPointer(e);

  auto sew = op->typeInfo->sew.to_int();

  #pragma push_macro("VI_VFP_VF_LOOP")
  #undef VI_VFP_VF_LOOP
  #define VI_VFP_VF_LOOP(BODY16, BODY32, BODY64)                               \\
  RIF::RawDatumOperand vd(dataA[i]);                                           \\
  RIF::RawDatumOperand rs1(*dataB);                                            \\
  RIF::RawDatumOperand vs2(dataC[i]);                                          \\
  switch (sew) {                                                               \\
  case e16:                                                                    \\
    BODY16;                                                                    \\
    break;                                                                     \\
  case e32:                                                                    \\
    BODY32;                                                                    \\
    break;                                                                     \\
  case e64:                                                                    \\
    BODY64;                                                                    \\
    break;                                                                     \\
  default:                                                                     \\
    assert(0);                                                                 \\
    break;                                                                     \\
  }                                                                            \\
  dataOut[i] = vd;

  #pragma push_macro("VI_VFP_VF_LOOP_WIDE")
  #undef VI_VFP_VF_LOOP_WIDE
  #define VI_VFP_VF_LOOP_WIDE(BODY16, BODY32)                                  \\
  RIF::RawDatumOperand vd(dataA[i]);                                           \\
  RIF::RawDatumOperand rs1(*dataB);                                            \\
  RIF::RawDatumOperand vs2(dataC[i]);                                          \\
  switch (sew) {                                                               \\
  case e16:                                                                    \\
    vs2 = f16_to_f32(vs2);                                                     \\
    rs1 = f16_to_f32(rs1);                                                     \\
    BODY16;                                                                    \\
    break;                                                                     \\
  case e32:                                                                    \\
    vs2 = f32_to_f64(vs2);                                                     \\
    rs1 = f32_to_f64(rs1);                                                     \\
    BODY32;                                                                    \\
    break;                                                                     \\
  default:                                                                     \\
    assert(0);                                                                 \\
    break;                                                                     \\
  }                                                                            \\
  dataOut[i] = vd;

  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''

vx_literal_mask_destructive_body_frm = '''
  assert(a->length == b->length && a->length == d->length &&
          a->length == f->length && c->length == 1);

  auto length = a->length;

  auto dataM = getRawPointer(a); //vm
  auto dataA = getRawPointer(b); //vd
  auto dataB = getRawPointer(c); //rs1
  auto dataC = getRawPointer(d); //vs2
  auto dataD = {}; //frm
  auto dataOut = getRawPointer(f);

  auto frm = dataD;
  P.VU.set_fround_mode(frm);
  auto sew = op->typeInfo->sew.to_int();
'''

vx_literal_mask_destructive_widen_body_frm = '''
// script/VXLiteral.py vx_literal_mask_destructive_widen_body_frm
  assert(a->length == b->length && a->length == c->length && d->length == 1);

  auto length = a->length;

  auto dataM = getRawPointer(a); //vm
  auto dataA = getRawPointer(b); //vd
  auto dataB = getRawPointer(c); //rs1
  auto dataC = getRawPointer(d); //vs2
  auto dataD = {}; //frm
  auto dataOut = getRawPointer(f);

  auto frm = dataD;
  P.VU.set_fround_mode(frm);
  auto sew = op->typeInfo->sew.to_int();
'''

vx_literal_vxrm_rounding = '''
    dataOut[i] = f{}_roundToInt(dataOut[i], vxrm, true);
'''

vx_literal_frm_rounding = '''
    dataOut[i] = f{}_roundToInt(dataOut[i], frm, true);
'''

vx_literal_mask_destructive_body_vxrm = '''
  assert(a->length == b->length && a->length == d->length &&
          a->length == f->length && c->length == 1);

  auto length = a->length;

  auto dataM = getRawPointer(a); //vm
  auto dataA = getRawPointer(b); //vd
  auto dataB = getRawPointer(c); //rs1
  auto dataC = getRawPointer(d); //vs2
  auto dataD = {}; //vxrm
  auto dataOut = getRawPointer(f);

  auto vxrm = dataD;
  P.VU.set_vround_mode(vxrm);
  auto sew = op->typeInfo->sew.to_int();
  '''

vx_literal_destructive_body_macro = '''
  #pragma push_macro("VI_VFP_VF_LOOP")
  #undef VI_VFP_VF_LOOP
  #define VI_VFP_VF_LOOP(BODY16, BODY32, BODY64)                               \\
  RIF::RawDatumOperand vd(dataA[i]);                                           \\
  RIF::RawDatumOperand rs1(*dataB);                                            \\
  RIF::RawDatumOperand vs2(dataC[i]);                                          \\
  switch (sew) {                                                               \\
  case e16:                                                                    \\
    BODY16;                                                                    \\
    break;                                                                     \\
  case e32:                                                                    \\
    BODY32;                                                                    \\
    break;                                                                     \\
  case e64:                                                                    \\
    BODY64;                                                                    \\
    break;                                                                     \\
  default:                                                                     \\
    assert(0);                                                                 \\
    break;                                                                     \\
  }                                                                            \\
  dataOut[i] = vd;

  #pragma push_macro("VI_VFP_VF_LOOP_WIDE")
  #undef VI_VFP_VF_LOOP_WIDE
  #define VI_VFP_VF_LOOP_WIDE(BODY16, BODY32)                                  \\
  RIF::RawDatumOperand vd(dataA[i]);                                           \\
  RIF::RawDatumOperand rs1(*dataB);                                            \\
  RIF::RawDatumOperand vs2(dataC[i]);                                          \\
  switch (sew) {                                                               \\
  case e16:                                                                    \\
    vs2 = f16_to_f32(vs2);                                                     \\
    rs1 = f16_to_f32(rs1);                                                     \\
    BODY16;                                                                    \\
    break;                                                                     \\
  case e32:                                                                    \\
    vs2 = f32_to_f64(vs2);                                                     \\
    rs1 = f32_to_f64(rs1);                                                     \\
    BODY32;                                                                    \\
    break;                                                                     \\
  default:                                                                     \\
    assert(0);                                                                 \\
    break;                                                                     \\
  }                                                                            \\
  dataOut[i] = vd;

  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''

vx_literal_mask_end = '''
    }else{
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
    }
  }
}
'''

vx_literal_mask_bool_end= '''
    }else {
      dataOut[i] = 1;
    }
  }
}
'''

vx_ta_literal_mask_end = '''
    } else
      dataOut[i] = dataMO[i];
  }
  auto half = length / 2;
  for (int i = half; i < length; ++i) {
    dataOut[i] = -1;
  }
}
'''

vx_tu_literal_mask_end = '''
    } else
      dataOut[i] = dataMO[i];
  }
  auto half = length / 2;
  for (int i = half; i < length; ++i) {
    dataOut[i] = dataMO[i];
  }
}
'''

vx_literal_mask_destructive_end = '''
    }else{
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
    }
  }
  #pragma pop_macro("VI_VFP_VF_LOOP")
  #pragma pop_macro("VI_VFP_VF_LOOP_WIDE")
}
'''

vx_literal_masked_no_maskedoff_body = '''
  auto length = a->length;

  auto dataM = getRawPointer(a);
  auto dataA = getRawPointer(b);
  auto dataB = getRawPointer(c);
  auto dataOut = getRawPointer(d);

  auto sew = op->typeInfo->sew.to_int();
  auto dataASew = b->typeInfo->sew.to_int(); // for index load / store only
  P.VU.vsew = sew;

  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''

vx_literal_masked_no_masked_off_end = '''
    } else {

    }
  }
}
'''

vx_tama_literal_mask_end = '''
    } else { // maskedoff element is agnostic
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
    }
  }
  for (int i = 0; i < length; ++i) {
    if (i & 1) // tail element is agnostic
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
  }
}
'''

vx_tamu_literal_mask_end = '''
    } else { // maskedoff element is undisturbed
      dataOut[i] = dataMO[i];
    }
  }
  for (int i = 0; i < length; ++i) {
    if (i & 1) // tail element is agnostic
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
  }
}
'''

vx_tuma_literal_mask_end = '''
    } else { // maskedoff element is agnostic
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
    }
  }
  for (int i = 0; i < length; ++i) {
    if (i & 1) // tail element is undisturbed
      dataOut[i] = dataMO[i];
  }
}
'''

vx_tumu_literal_mask_end = '''
    } else { // maskedoff element is undisturbed
      dataOut[i] = dataMO[i];
    }
  }
  for (int i = 0; i < length; ++i) {
    if (i & 1) // tail element is undisturbed
      dataOut[i] = dataMO[i];
  }
}
'''

vx_tama_literal_mask_destructive_end = '''
    } else // maskedoff element is agnostic
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
  }
  #pragma pop_macro("VI_VFP_VF_LOOP")
  #pragma pop_macro("VI_VFP_VF_LOOP_WIDE")
}
'''

vx_tamu_literal_mask_destructive_end = '''
    } else // maskedoff element is undisturbed
      dataOut[i] = dataMO[i];
  }
  #pragma pop_macro("VI_VFP_VF_LOOP")
  #pragma pop_macro("VI_VFP_VF_LOOP_WIDE")
  for (int i = 0; i < length; ++i) {
    if (i & 1) // tail element is agnostic
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
  }
}
'''

vx_tuma_literal_mask_destructive_end = '''
    } else // maskedoff element is agnostic
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
  }
  #pragma pop_macro("VI_VFP_VF_LOOP")
  #pragma pop_macro("VI_VFP_VF_LOOP_WIDE")
  for (int i = 0; i < length; ++i) {
    if (i & 1) // tail element is undisturbed
      dataOut[i] = dataMO[i];
  }
}
'''

vx_tumu_literal_mask_destructive_end = '''
    } else // maskedoff element is undisturbed
      dataOut[i] = dataMO[i];
  }
  #pragma pop_macro("VI_VFP_VF_LOOP")
  #pragma pop_macro("VI_VFP_VF_LOOP_WIDE")
  for (int i = 0; i < length; ++i) {
    if (i & 1) // tail element is undisturbed
      dataOut[i] = dataMO[i];
  }
}
'''

vx_mu_literal_masked_no_maskedoff_body = '''
  auto length = a->length;

  auto dataPassthru = getRawPointer(a);
  auto dataM = getRawPointer(b);
  auto dataA = getRawPointer(c);
  auto dataB = getRawPointer(d);
  auto dataOut = getRawPointer(e);

  auto sew = op->typeInfo->sew.to_int();
  auto dataASew = b->typeInfo->sew.to_int(); // for index load / store only
  P.VU.vsew = sew;

  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''

vx_ma_literal_masked_no_masked_off_end = '''
    } else { // maskedoff element is agnostic
      memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
    }
  }
}
'''

vx_mask_output_ma_literal_masked_no_masked_off_end = '''
    } else { // maskedoff element is agnostic(only set one bit)
      dataOut[i] = 1;
    }
  }
}
'''

vx_mu_literal_masked_no_masked_off_end = '''
    } else { // maskedoff element is undisturbed
      dataOut[i] = dataPassthru[i];
    }
  }
}
'''


def include_literal(filename):
    return "#include\"" + filename + "\""

def create_wf_op(op_type, op_id, sew, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += vx_literal_start0 + op_type + vx_literal_start1
  for i in range(input_num) :
    var = chr(ord('a') + i)
    ret += "  auto " + var + " = static_cast<RIF::" + input_types[i] + "Val *>(op->inputs[" + str(i) + "]);\n"
  var = chr(ord('a') + input_num)
  ret += "  auto " + var + " = static_cast<RIF::" + output_type + "Val *>(op->outputs[0]);\n"
  if "MaskedOperation" in op_attr :
    if "FRM" in op_attr :
      if "frm0" in op_attr :
        frm = 0
      elif "frm1" in op_attr :
        frm = 1
      elif "frm2" in op_attr :
        frm = 2
      elif "frm3" in op_attr :
        frm = 3
      elif "frm4" in op_attr :
        frm = 4
      ret += wf_literal_masked_frm_body.format(frm) + mask_loop_start + include_literal("v" + op_id + ".h") + vx_literal_mask_end
    else:
      if output_type == "OneDBool":
        ret += vx_literal_mask_body + include_literal("v" + op_id + ".h") + vx_literal_mask_bool_end
      else:
        ret += vx_literal_mask_body + include_literal("v" + op_id + ".h") + vx_literal_mask_end
  else :
    if "FRM" in op_attr :
      if "frm0" in op_attr :
        frm = 0
      elif "frm1" in op_attr :
        frm = 1
      elif "frm2" in op_attr :
        frm = 2
      elif "frm3" in op_attr :
        frm = 3
      elif "frm4" in op_attr :
        frm = 4
      ret += wf_literal_nonmasked_frm_body.format(frm) + loop_start + include_literal("v" + op_id + ".h") + vx_literal_nonmask_end
    else :
      ret += vx_literal_nonmask_body + include_literal("v" + op_id + ".h") + vx_literal_nonmask_end
  return ret

def create_vx_op(op_type, op_id, sew, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += vx_literal_start0 + op_type + vx_literal_start1
  for i in range(input_num) :
    var = chr(ord('a') + i)
    ret += "  auto " + var + " = static_cast<RIF::" + input_types[i] + "Val *>(op->inputs[" + str(i) + "]);\n"
  var = chr(ord('a') + input_num)
  ret += "  auto " + var + " = static_cast<RIF::" + output_type + "Val *>(op->outputs[0]);\n"
  if "MaskedOperation" in op_attr :
    if "TailAgnostic" in op_attr and "MaskAgnostic" in op_attr : # tama
      ret += vx_literal_masked_no_maskedoff_body + include_literal("v" + op_id + ".h") + vx_tama_literal_mask_end
    elif "VXRM" in op_attr : # vxrm
      if "vxrm0" in op_attr :
        vxrm = 0
      elif "vxrm1" in op_attr :
        vxrm = 1
      elif "vxrm2" in op_attr :
        vxrm = 2
      elif "vxrm3" in op_attr :
        vxrm = 3
      ret += vx_literal_mask_vxrm_body.format(vxrm) + mask_loop_start + include_literal("v" + op_id + ".h") + vx_literal_mask_end
    elif "FRM" in op_attr and "MulAddOperation" not in op_attr and "WideningOperation" not in op_attr: # frm
      if "frm0" in op_attr :
        frm = 0
      elif "frm1" in op_attr :
        frm = 1
      elif "frm2" in op_attr :
        frm = 2
      elif "frm3" in op_attr :
        frm = 3
      elif "frm4" in op_attr :
        frm = 4
      ret += vx_literal_masked_frm_body.format(frm) + mask_loop_start + include_literal("v" + op_id + ".h") + vx_literal_frm_rounding.format(sew) + vx_literal_mask_end
    elif "TailAgnostic" in op_attr and "MaskUndisturbed" in op_attr : # tamu
      ret += vx_literal_mask_body + include_literal("v" + op_id + ".h") + vx_tamu_literal_mask_end
    elif "TailUndisturbed" in op_attr and "MaskAgnostic" in op_attr : # tuma
      ret += vx_literal_mask_body + include_literal("v" + op_id + ".h") + vx_tuma_literal_mask_end
    elif "TailUndisturbed" in op_attr and "MaskUndisturbed" in op_attr : # tumu
      ret += vx_literal_mask_body + include_literal("v" + op_id + ".h") + vx_tumu_literal_mask_end
    else : # No explicit policy specified
      if output_type == "OneDBool":
        ret += vx_literal_mask_body + include_literal("v" + op_id + ".h") + vx_literal_mask_bool_end
      else:
        ret += vx_literal_mask_body + include_literal("v" + op_id + ".h") + vx_literal_mask_end
  else :
    if "TailUndisturbed" in op_attr :
      ret += vx_tu_literal_nonmask_body + include_literal("v" + op_id + ".h") + vx_tu_literal_nonmask_end
    elif "VXRM" in op_attr:
      if "vxrm0" in op_attr :
        vxrm = 0
      elif "vxrm1" in op_attr :
        vxrm = 1
      elif "vxrm2" in op_attr :
        vxrm = 2
      elif "vxrm3" in op_attr :
        vxrm = 3
      ret += vx_literal_nonmask_vxrm_body.format(vxrm) + loop_start +include_literal("v" + op_id + ".h") + vx_literal_nonmask_end
    elif "FRM" in op_attr and ("MulAddOperation" in op_attr):
      if "frm0" in op_attr :
        frm = 0
      elif "frm1" in op_attr :
        frm = 1
      elif "frm2" in op_attr :
        frm = 2
      elif "frm3" in op_attr :
        frm = 3
      elif "frm4" in op_attr :
        frm = 4
      ret += vx_literal_nonmask_MulAddOperation_destructive_body_frm.format(frm) + vx_literal_nonmask_destructive_macro_frm + loop_start + include_literal("v" + op_id + ".h") + vx_literal_frm_rounding.format(sew) + vx_literal_nonmask_end
    elif "FRM" in op_attr and "MulAddOperation" not in op_attr and "WideningOperation" not in op_attr: # frm
      if "frm0" in op_attr :
        frm = 0
      elif "frm1" in op_attr :
        frm = 1
      elif "frm2" in op_attr :
        frm = 2
      elif "frm3" in op_attr :
        frm = 3
      elif "frm4" in op_attr :
        frm = 4
      ret += vx_literal_nonmask_destructive_body_frm.format(frm) + loop_start + include_literal("v" + op_id + ".h") + vx_literal_frm_rounding.format(sew) + vx_literal_nonmask_end
    elif "TailAgnostic" in op_attr :
      ret += vx_literal_nonmask_body + include_literal("v" + op_id + ".h") + vx_ta_literal_nonmask_end
    else :
      ret += vx_literal_nonmask_body + include_literal("v" + op_id + ".h") + vx_literal_nonmask_end
  return ret

def create_destructive_vx_op(op_type, op_id, op_sew, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += vx_literal_start0 + op_type + vx_literal_start1
  for i in range(input_num) :
    var = chr(ord('a') + i)
    ret += "  auto " + var + " = static_cast<RIF::" + input_types[i] + "Val *>(op->inputs[" + str(i) + "]);\n"
  var = chr(ord('a') + input_num)
  ret += "  auto " + var + " = static_cast<RIF::" + output_type + "Val *>(op->outputs[0]);\n"
  if "MaskedOperation" in op_attr :
    if "TailAgnostic" in op_attr and "MaskAgnostic" in op_attr : # tama
      ret += vx_literal_mask_destructive_body  + include_literal("v" + op_id + ".h") + vx_tama_literal_mask_destructive_end
    elif "TailAgnostic" in op_attr and "MaskUndisturbed" in op_attr : # tamu
      ret += vx_literal_mask_destructive_body + include_literal("v" + op_id + ".h") + vx_tamu_literal_mask_destructive_end
    elif "TailUndisturbed" in op_attr and "MaskAgnostic" in op_attr : # tuma
      ret += vx_literal_mask_destructive_body + include_literal("v" + op_id + ".h") + vx_tuma_literal_mask_destructive_end
    elif "TailUndisturbed" in op_attr and "MaskUndisturbed" in op_attr : # tumu
      ret += vx_literal_mask_destructive_body + include_literal("v" + op_id + ".h") + vx_tumu_literal_mask_destructive_end
    elif  "FRM" in op_attr and "WideningOperation" not in op_attr and "MulAddOperation" not in op_attr: # frm
      if "frm0" in op_attr :
        frm = 0
      elif "frm1" in op_attr :
        frm = 1
      elif "frm2" in op_attr :
        frm = 2
      elif "frm3" in op_attr :
        frm = 3
      elif "frm4" in op_attr :
        frm = 4
      ret += vx_literal_mask_destructive_body_frm.format(frm) + vx_literal_destructive_body_macro + include_literal("v" + op_id + ".h") + vx_literal_frm_rounding.format(widen_sew) + vx_tama_literal_mask_destructive_end
    elif  "FRM" in op_attr and ("WideningOperation" in op_attr or "MulAddOperation" in op_attr) : # frm
      if "WideningOperation" in op_attr or op_id == "fwmsac_vf" or op_id == "fwnmsac_vf" or op_id == "fwmacc_vf" or op_id == "fwnmacc_vf":
        if int(op_sew) <= 32:
          widen_sew = 2 * int(op_sew) # WideningOperation
        else:
          widen_sew = 64
      else:
        widen_sew = int(op_sew)
      if "frm0" in op_attr :
        frm = 0
      elif "frm1" in op_attr :
        frm = 1
      elif "frm2" in op_attr :
        frm = 2
      elif "frm3" in op_attr :
        frm = 3
      elif "frm4" in op_attr :
        frm = 4
      ret += vx_literal_mask_destructive_widen_body_frm.format(frm) + vx_literal_destructive_body_macro + include_literal("v" + op_id + ".h") + vx_literal_frm_rounding.format(widen_sew) + vx_tama_literal_mask_destructive_end
    elif "VXRM" in op_attr : # vxrm
      if "vxrm0" in op_attr :
        vxrm = 0
      elif "vxrm1" in op_attr :
        vxrm = 1
      elif "vxrm2" in op_attr :
        vxrm = 2
      elif "vxrm3" in op_attr :
        vxrm = 3
      ret += vx_literal_mask_destructive_body_vxrm.format(vxrm) + vx_literal_destructive_body_macro + mask_loop_start + include_literal("v" + op_id + ".h") + vx_literal_vxrm_rounding.format(sew) + vx_literal_mask_destructive_end
    else : # No explicit policy specified
      ret += vx_literal_mask_destructive_body + include_literal("v" + op_id + ".h") + vx_literal_mask_destructive_end
  else :
    if "TailUndisturbed" in op_attr :
      ret += vx_literal_nonmask_destructive_body + include_literal("v" + op_id + ".h") + vx_tu_literal_nonmask_destructive_end
    elif "TailAgnostic" in op_attr :
      ret += vx_literal_nonmask_destructive_body + include_literal("v" + op_id + ".h") + vx_ta_literal_nonmask_destructive_end
    elif "FRM" in op_attr and "WideningOperation" not in op_attr and "MulAddOperation" not in op_attr:
      if "frm0" in op_attr :
        frm = 0
      elif "frm1" in op_attr :
        frm = 1
      elif "frm2" in op_attr :
        frm = 2
      elif "frm3" in op_attr :
        frm = 3
      elif "frm4" in op_attr :
        frm = 4
      ret += vx_literal_nonmask_destructive_body_frm.format(frm) + loop_start + include_literal("v" + op_id + ".h") + vx_literal_frm_rounding.format(sew) + vx_literal_nonmask_destructive_end
    elif "FRM" in op_attr and ("WideningOperation" in op_attr or "MulAddOperation" in op_attr):
      if "WideningOperation" in op_attr or op_id == "fwmsac_vf" or op_id == "fwnmsac_vf" or op_id == "fwmacc_vf" or op_id == "fwnmacc_vf":
        if int(op_sew) <= 32:
          widen_sew = 2 * int(op_sew) # WideningOperation
        else:
          widen_sew = 64
      else:
        widen_sew = int(op_sew)
      if "frm0" in op_attr :
        frm = 0
      elif "frm1" in op_attr :
        frm = 1
      elif "frm2" in op_attr :
        frm = 2
      elif "frm3" in op_attr :
        frm = 3
      elif "frm4" in op_attr :
        frm = 4
      ret += vx_literal_nonmask_widen_destructive_body_frm.format(frm) + vx_literal_nonmask_destructive_macro_frm + loop_start + include_literal("v" + op_id + ".h") + vx_literal_frm_rounding.format(widen_sew) + vx_literal_nonmask_destructive_end
    elif "VXRM" in op_attr:
      if "vxrm0" in op_attr :
        vxrm = 0
      elif "vxrm1" in op_attr :
        vxrm = 1
      elif "vxrm2" in op_attr :
        vxrm = 2
      elif "vxrm3" in op_attr :
        vxrm = 3
      ret += vx_literal_nonmask_destructive_body_vxrm.format(vxrm) + vx_literal_destructive_body_macro + loop_start + include_literal("v" + op_id + ".h") + vx_literal_vxrm_rounding.format(sew) + vx_literal_nonmask_destructive_end
    else :
      ret += vx_literal_nonmask_destructive_body + include_literal("v" + op_id + ".h") + vx_literal_nonmask_destructive_end
  return ret

def create_masked_no_maskedoff_vx_op(op_type, op_id, sew, op_attr, output_type, input_num, input_nfield, output_nfield, input_types) :
  ret = ""
  ret += vx_literal_start0 + op_type + vx_literal_start1
  for i in range(input_num) :
    var = chr(ord('a') + i)
    ret += "  auto " + var + " = static_cast<RIF::" + input_types[i] + "Val *>(op->inputs[" + str(i) + "]);\n"
  var = chr(ord('a') + input_num)
  ret += "  auto " + var + " = static_cast<RIF::" + output_type + "Val *>(op->outputs[0]);\n"
  if "MaskAgnostic" in op_attr : # ma
    ret += vx_literal_masked_no_maskedoff_body  + include_literal("v" + op_id + ".h")
    if op_type[-3:] == "_MA" : # output is mask(only one bit for each element)
      ret += vx_mask_output_ma_literal_masked_no_masked_off_end
    else :
      ret += vx_ma_literal_masked_no_masked_off_end
  elif "MaskUndisturbed" in op_attr : # mu
    ret += vx_mu_literal_masked_no_maskedoff_body + include_literal("v" + op_id + ".h") + vx_mu_literal_masked_no_masked_off_end
  else :
    ret += vx_literal_masked_no_maskedoff_body + include_literal("v" + op_id + ".h") + vx_literal_masked_no_masked_off_end
  return ret
