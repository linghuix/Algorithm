# CMakeLists.txt 文件并不区分命令的大小写
# cmake　最低版本需求
cmake_minimum_required(VERSION 3.10)

# set the project name, the bin file we get finally
# 最后生成的可执行文件名称，也叫项目名称。为可执行文件和项目提供一个版本号
project(Shortest_rode VERSION 1.0)


SET(CMAKE_SOURCE_DIR .)
 
SET(CMAKE_MODULE_PATH ${CMAKE_ROOT}/Modules ${CMAKE_SOURCE_DIR}/cmake/modules)

# add .h and .c
AUX_SOURCE_DIRECTORY(. DIR_SRCS)
#set(my_include_path, )
# 向工程添加多个特定的头文件搜索路径,路径之间用空格分割
# INCLUDE_DIRECTORIES("/mnt/Documents/100-语言/S6-C/1-C_code/0-数据结构/2-堆栈/顺序存储结构的栈/Stack")
#add_subdirectory("/mnt/Documents/100-语言/S6-C/1-C_code/0-数据结构/2-堆栈/顺序存储结构的栈/Stack")

# add the executable
ADD_EXECUTABLE(main ${DIR_SRCS})

FIND_PACKAGE( libstructure_cxx REQUIRED)

MARK_AS_ADVANCED(
libstructure_cxx_INCLUDE_DIR
LIBDB_CXX_LIBRARIES
)
IF (libstructure_cxx_INCLUDE_DIR AND LIBDB_CXX_LIBRARIES)
MESSAGE(STATUS "Found libdb libraries")

INCLUDE_DIRECTORIES(${libstructure_cxx_INCLUDE_DIR})

MESSAGE(  ${LIBDB_CXX_LIBRARIES} )
MESSAGE(  ${libstructure_cxx_INCLUDE_DIR} )

TARGET_LINK_LIBRARIES( main ${LIBDB_CXX_LIBRARIES} )

ENDIF (libstructure_cxx_INCLUDE_DIR AND LIBDB_CXX_LIBRARIES)


