cmake_minimum_required(VERSION 2.8.12)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

if(MSVC AND MSVC_VERSION EQUAL 1800)
  add_definitions("-Dinline=__inline")
endif()

add_subdirectory("source_subfolder")
