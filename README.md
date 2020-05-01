# Core Flight System : Framework : Tool : ELF to cFE Table Converter

This repository contains NASA's ELF to cFE Table Converter Tool (elf2cfetbl), which is a framework component of the Core Flight System.

This lab application is a ground utility to convert ELF to cFE binary tables for cFS. It is intended to be located in the `tools/elf2cfetbl` subdirectory of a cFS Mission Tree.  The Core Flight System is bundled at https://github.com/nasa/cFS (which includes this tool as a submodule), which includes build and execution instructions.

See README.txt for more information.

## Version History

#### Development Build: 3.1.3
  
- Builds for vxworks w/ 32-bit host
- See https://github.com/nasa/elf2cfetbl/pull/40

#### Development Build: 3.1.2
  
- Minor bug fixes and documentation (see https://github.com/nasa/elf2cfetbl/pull/25)

#### Development Build: 3.1.1

- Minor updates (see https://github.com/nasa/elf2cfetbl/pull/19)


### ***OFFICIAL RELEASE: 3.1.0***

- Minor updates (see https://github.com/nasa/elf2cfetbl/pull/13)
- Not backwards compatible with OSAL 4.2.1
- Released as part of cFE 6.7.0, Apache 2.0

### ***OFFICIAL RELEASE: 3.0a***

- Released as part of cFE 6.6.0a, Apache 2.0

NOTE - there are other parameter set management schemes used with the cFS (JSON, csv, etc) which may be more applicable for modern missions.  Contact the community as detailed below for more information.

## Known issues

This ground utility was developed for a specific mission/configuration, and may not be applicable for general use.  The Makefile and for_build/Makefile are no longer supported or tested.

## Getting Help

For best results, submit issues:questions or issues:help wanted requests at https://github.com/nasa/cFS.

Official cFS page: http://cfs.gsfc.nasa.gov

