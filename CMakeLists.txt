cmake_minimum_required(VERSION 3.25)

project(lua)

set(LUA_VERSION "5.4.8" CACHE STRING "Desired lua version")
set(LUA_FTP_URL "https://www.lua.org/ftp/lua-${LUA_VERSION}.tar.gz")
option(LINK_INTERPRETER_SHARED "Link shared lib to interpreter" ON)

set(PYTHON_EXEC python)
if(UNIX)
    set(PYTHON_EXEC python3)
endif()

macro(download_lua)
    if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lua.tar.gz")
        message(STATUS "Downloading Lua version ${LUA_VERSION} from ${LUA_FTP_URL}")
        execute_process(COMMAND python "${CMAKE_CURRENT_SOURCE_DIR}/downloader.py" ${LUA_FTP_URL} ${CMAKE_CURRENT_SOURCE_DIR})
    else()
        message(STATUS "Lua version ${LUA_VERSION} already exists, skipping download.")
    endif()
endmacro()

download_lua()

set(LIB_BASE_SOURCES lapi.c lcode.c lctype.c ldebug.c ldo.c ldump.c lfunc.c lgc.c 
                     llex.c lmem.c lobject.c lopcodes.c lparser.c lstate.c lstring.c ltable.c 
                     ltm.c lundump.c lvm.c lzio.c lauxlib.c lbaselib.c lcorolib.c ldblib.c liolib.c 
                     lmathlib.c loadlib.c loslib.c lstrlib.c ltablib.c lutf8lib.c linit.c)

foreach(SRC ${LIB_BASE_SOURCES})
    set(LUA_SRCS ${LUA_SRCS} "lua-${LUA_VERSION}/src/${SRC}")
endforeach(SRC ${LIB_BASE_SOURCES})

set(INTERPRETER_SOURCE "lua-${LUA_VERSION}/src/lua.c")
set(COMPILER_SOURCE "lua-${LUA_VERSION}/src/luac.c")

add_library(lualibs STATIC ${LUA_SRCS})
target_include_directories(lualibs PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/lua-${LUA_VERSION}/src> 
                                      $<INSTALL_INTERFACE:include>)

add_library(lualib SHARED ${LUA_SRCS})
target_include_directories(lualib PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/lua-${LUA_VERSION}/src> 
                                      $<INSTALL_INTERFACE:include>)

if(WIN32)
    target_compile_definitions(lualib PUBLIC LUA_BUILD_AS_DLL PRIVATE)
endif()

if(LINUX)
    target_link_libraries(lualibs PUBLIC m)
    target_link_libraries(lualib PUBLIC m)
endif()

add_executable(lua ${INTERPRETER_SOURCE})
if(LINK_INTERPRETER_SHARED)
    target_link_libraries(lua lualib)
else()
    target_link_libraries(lua lualibs)
endif()

add_executable(luac ${COMPILER_SOURCE})
target_link_libraries(luac lualibs)

set(LUA_GENERATED_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(LUA_VERSION_CONFIG "${LUA_GENERATED_DIR}/luaConfigVersion.cmake")
set(LUA_PROJECT_CONFIG "${LUA_GENERATED_DIR}/luaConfig.cmake")
set(LUA_TARGETS_EXPORT_NAME "luaTargets")
set(LUA_CONFIG_INSTALL_DIR "lib/cmake/lua")
set(LUA_NAMESPACE "lua")

include(CMakePackageConfigHelpers)
write_basic_package_version_file("${LUA_VERSION_CONFIG}" VERSION ${LUA_VERSION} COMPATIBILITY SameMajorVersion)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/config.cmake.in" "${LUA_PROJECT_CONFIG}" @ONLY)

install(
    FILES ${LUA_PROJECT_CONFIG} ${LUA_VERSION_CONFIG}
    DESTINATION ${LUA_CONFIG_INSTALL_DIR})
install(
    EXPORT "${LUA_TARGETS_EXPORT_NAME}"
    NAMESPACE ${LUA_NAMESPACE}::
    DESTINATION ${LUA_CONFIG_INSTALL_DIR})

install(TARGETS lualib lua luac lualibs
        EXPORT luaTargets
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(FILES lua-${LUA_VERSION}/src/lua.h lua-${LUA_VERSION}/src/luaconf.h lua-${LUA_VERSION}/src/lualib.h lua-${LUA_VERSION}/src/lauxlib.h lua-${LUA_VERSION}/src/lua.hpp
        DESTINATION include/lua${LUA_VERSION})

