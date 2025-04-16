include_directories(${INC})
include_directories(${SOFTFLOAT}/include)

add_test(
  NAME Golden.Codegen
  COMMAND python3 ${CMAKE_SOURCE_DIR}/scripts/TestCodeGen.py
                  --random-gen=${CMAKE_BINARY_DIR}/tool/random_gen
                  --filepath=${CMAKE_SOURCE_DIR}/include/CustomOperator.def
                  --codegen-golden=${CMAKE_SOURCE_DIR}/test/codegen-golden
                  --output-dir=${CMAKE_BINARY_DIR}/codegen-output
                  --has-policy
)

set(GCC_TOOLCHAIN_PREFIX "/sifive/tools/riscv-tools/riscv64-unknown-linux-gnu-toolsuite-13.0.0-2021.11.5-x86_64-linux-redhat8")
set(COMPILER_TOOLCHAIN_PREFIX "/sifive/tools/riscv-tools/riscv64-unknown-linux-gnu-toolsuite-13.0.0-2021.11.5-x86_64-linux-redhat8")
set(FUZZ 1)
set(NODE 20)
set(LENGTH 50)
set(ENABLE_FUSED_GEN 1)
set(RANDOM_OR_SEED "--random on")
if(DEFINED ENV{GCC_TOOLCHAIN_PREFIX})
  set(GCC_TOOLCHAIN_PREFIX $ENV{GCC_TOOLCHAIN_PREFIX})
elseif(DEFINED ENV{TOOLCHAIN_PATH})
  set(GCC_TOOLCHAIN_PREFIX $ENV{TOOLCHAIN_PATH})
endif()
if(DEFINED ENV{COMPILER_TOOLCHAIN_PREFIX})
  set(COMPILER_TOOLCHAIN_PREFIX $ENV{COMPILER_TOOLCHAIN_PREFIX})
elseif(DEFINED ENV{TOOLCHAIN_PATH})
  set(COMPILER_TOOLCHAIN_PREFIX $ENV{TOOLCHAIN_PATH})
endif()
if(DEFINED ENV{FUZZ})
  set(FUZZ $ENV{FUZZ})
endif()
if(DEFINED ENV{NODE})
  set(NODE $ENV{NODE})
endif()
if(DEFINED ENV{LENGTH})
  set(LENGTH $ENV{LENGTH})
endif()
if(DEFINED ENV{SEED})
  set(RANDOM_OR_SEED "--seed $ENV{SEED}")
endif()
if(DEFINED ENV{ENABLE_FUSED_GEN})
  set(ENABLE_FUSED_GEN "$ENV{ENABLE_FUSED_GEN}")
endif()

message(STATUS "GCC toolchain path: " ${GCC_TOOLCHAIN_PREFIX})
message(STATUS "LLVM toolchain path: " ${COMPILER_TOOLCHAIN_PREFIX})

set(GCC_TOOLCHAIN ${GCC_TOOLCHAIN_PREFIX}/bin/riscv64-unknown-linux-gnu-gcc)
execute_process(COMMAND ${GCC_TOOLCHAIN} --print-sysroot OUTPUT_VARIABLE SYSROOT OUTPUT_STRIP_TRAILING_WHITESPACE)

set(CLANG "${COMPILER_TOOLCHAIN_PREFIX}/bin/riscv64-unknown-linux-gnu-clang")
set(CFLAGS "-target riscv64-unknown-linux-gnu --sysroot ${SYSROOT} --gcc-toolchain=${GCC_TOOLCHAIN_PREFIX}")
set(POLICY_ENABLE "")

if("${OK}" STREQUAL "0")
  set(POLICY_ENABLE "--has-policy")
endif()

foreach(count RANGE 1 ${FUZZ})
  add_test(
    NAME Test.FuzzTestRandomGen${count}
    COMMAND
    sh -c "rm -rf fuzz_test_random_gen${count} && mkdir fuzz_test_random_gen${count} && cd fuzz_test_random_gen${count} && \
    ${CMAKE_SOURCE_DIR}/rif-test --gen-path ${CMAKE_BINARY_DIR}/tool --sim ${CMAKE_SOURCE_DIR}/prebuilt/metal-run/qemu-run --cc ${CLANG} --arch rv64gcv_zfh_zvfh0p1 --cflags \"${CFLAGS}\" ${POLICY_ENABLE} --node ${NODE} --length ${LENGTH} ${RANDOM_OR_SEED} && \
    make -j$(nproc)"
  )
endforeach()

if("${ENABLE_FUSED_GEN}" STREQUAL "1")
  foreach(count RANGE 1 ${FUZZ})
    add_test(
      NAME Test.FuzzTestFusedGen${count}
      COMMAND
      sh -c "rm -rf fuzz_test_fused_gen${count} && mkdir fuzz_test_fused_gen${count} && cd fuzz_test_fused_gen${count} && \
      ${CMAKE_SOURCE_DIR}/rif-test --gen fused_gen --gen-path ${CMAKE_BINARY_DIR}/tool --sim ${CMAKE_SOURCE_DIR}/prebuilt/metal-run/qemu-run --cc ${CLANG} --arch rv64gcv_zfh_zvfh0p1 --cflags \"${CFLAGS}\" ${POLICY_ENABLE} --node ${NODE} --length ${LENGTH} ${RANDOM_OR_SEED} && \
      make -j$(nproc)"
    )
  endforeach()
endif()
