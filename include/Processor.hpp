#ifndef RIF_PROCESSOR_H
#define RIF_PROCESSOR_H
#include <cstdint>

#ifdef __cplusplus
extern "C" {
#endif
// declare the C softfloat global so C++ can write it
extern uint_fast8_t softfloat_roundingMode;
#ifdef __cplusplus
}
#endif

extern uint_fast8_t softfloat_roundingMode;
typedef uint64_t reg_t;

enum VRM {
  RNU = 0, // round-to-nearest-up
  RNE,     // round-to-nearest-even
  RDN,     // round-to-nearest-down
  ROD,     // round-to-nearest-odd
  INVALID_RM
};

enum FloatRM {
    // softfloat_round_near_even   = 0,
    // softfloat_round_minMag      = 1,
    // softfloat_round_min         = 2,
    // softfloat_round_max         = 3,
    // softfloat_round_near_maxMag = 4,
    // softfloat_round_odd         = 5
// 000 RNE Round to Nearest, ties to Even
// 001 RTZ  Round towards Zero
// 010 RDN Round Down (towards -∞)
// 011 RUP Round Up (towards +∞)
// 100 RMM Round to Nearest, ties to Max Magnitude
// 111 DYM
  RNE_FRM = 0,
  RTZ_FRM = 1,
  RDN_FRM = 2,
  RUP_FRM = 3,
  RMM_FRM = 4,
  DYN_FRM = 7,
  INVALID_FRM
};

struct Processor {
  struct VectorUnit {
    unsigned vsew;      // sew
    unsigned vlmul = 1;    // lmul, set to 1 as default
    unsigned vflmul = 1;   // flmul, set to 1 as default
    VRM xrm = VRM::RNU; // rounding mode
    uint64_t VLEN = 128;  // set cpu VLEN = 128, can be modified later
    uint64_t vlmax;
    VRM get_vround_mode() { return xrm; }
    VRM set_vround_mode(int mode) {
      if (mode >= RNU && mode < INVALID_RM)
        xrm = static_cast<VRM>(mode);
      else
        xrm = INVALID_RM;
      return xrm;
    }

    uint_fast8_t get_fround_mode() { return softfloat_roundingMode; }
    // Replace/implement this to also update the softfloat C global
    uint_fast8_t set_fround_mode(int mode) {
      // map and validate
      if (mode >= RNE_FRM && mode < INVALID_FRM) {
        softfloat_roundingMode = mode;
      } else {
        softfloat_roundingMode = INVALID_FRM;
      }
      return softfloat_roundingMode;
    }

    // vector element for various SEW
    template <class T> T& elt(void* vReg, uint64_t n, bool is_write = false) {
      T* vRegPtr = reinterpret_cast<T*>(vReg);
      return vRegPtr[n];
    }
  };
  VectorUnit VU;
};

extern Processor P;
extern Processor *p;

#endif