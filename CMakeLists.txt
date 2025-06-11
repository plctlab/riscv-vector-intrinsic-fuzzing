cmake_minimum_required(VERSION 3.13.4)

project(vector-intrinsic-fuzzing LANGUAGES CXX C)

set_property(GLOBAL PROPERTY C_STANDARD 11)
set_property(GLOBAL PROPERTY CXX_STANDARD 17)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 17)
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -save-temps=obj -fsanitize=address ")
set(CMAKE_VERBOSE_MAKEFILE ON)

set(INC ${CMAKE_CURRENT_LIST_DIR}/include)
set(SPIKE ${CMAKE_CURRENT_LIST_DIR}/riscv-isa-sim)
set(LIB ${CMAKE_CURRENT_LIST_DIR}/library)
set(SOFTFLOAT ${CMAKE_CURRENT_LIST_DIR}/extern/riscv-softfloat-standalone)
set(METAL_RUN ${CMAKE_CURRENT_LIST_DIR}/prebuilt/metal-run)

execute_process(COMMAND git submodule update --init --recursive ${SOFTFLOAT} WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})
execute_process(COMMAND git submodule update --init --recursive ${METAL_RUN} WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})

add_custom_target(clean_headers
 COMMAND rm -rf ${CMAKE_CURRENT_SOURCE_DIR}/include/autogen
 COMMAND rm -rf ${CMAKE_CURRENT_SOURCE_DIR}/include/AutoGenComputeOp.h
 COMMENT "Clean header files with golden compute functions for operators"
)

add_custom_target(generate_headers ALL
 DEPENDS clean_headers
 COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/scripts/GenerateOperatorComputeHeaders.py ${CMAKE_CURRENT_SOURCE_DIR}
 COMMENT "Generate header files with golden compute functions for operators"
)

enable_testing()

add_subdirectory(extern)
add_subdirectory(include)
add_subdirectory(library)
add_subdirectory(tool)
