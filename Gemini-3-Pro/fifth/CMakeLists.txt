cmake_minimum_required(VERSION 3.16)

project(CppRichTextEditor VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ==========================================
# FIX: Enable Qt Meta-Object Compiler (MOC)
# ==========================================
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets Gui PrintSupport)

set(PROJECT_SOURCES
        main.cpp
        EditorWindow.cpp
        EditorWindow.h
)

add_executable(CppRichTextEditor ${PROJECT_SOURCES})

target_link_libraries(CppRichTextEditor PRIVATE Qt6::Widgets Qt6::Gui Qt6::PrintSupport)
