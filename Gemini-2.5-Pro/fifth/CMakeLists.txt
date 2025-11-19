# Minimum CMake version required
cmake_minimum_required(VERSION 3.16)

# Project name
project(RichTextEditor)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# This is required for Q_OBJECT macro and other Qt magic
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find the required Qt packages
find_package(Qt6 COMPONENTS Widgets REQUIRED)

# Add source files to the project
add_executable(RichTextEditor
    main.cpp
    mainwindow.cpp
    mainwindow.h
)

# Link the Qt libraries to the executable
target_link_libraries(RichTextEditor PRIVATE Qt6::Widgets)
