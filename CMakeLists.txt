cmake_minimum_required(VERSION 3.16)
set(PROJECT_VER "public-static-1.0")
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
idf_build_set_property(MINIMAL_BUILD ON)

project(FoloToy-AI-Passport)
