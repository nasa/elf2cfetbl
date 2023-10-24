# CMake snippet for building elf2cfetbl
#
include_directories(${MISSION_BINARY_DIR}/inc)
include_directories(${osal_MISSION_DIR}/src/os/inc)
include_directories(${cfe-core_MISSION_DIR}/src/inc)

add_executable(elf2cfetbl elf2cfetbl.c)

install(TARGETS elf2cfetbl DESTINATION host)

# The _XOPEN_SOURCE directive is required for glibc to enable conformance with the
# the X/Open standard version 6, which includes POSIX.1c as well as SUSv2/UNIX98 extensions.
# Needed in this target to get PATH_MAX in limits.h and ctime_r
target_compile_definitions(elf2cfetbl
    PRIVATE
    _XOPEN_SOURCE=600
 )
