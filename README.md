# Core Flight System : Framework : Tool : ELF to cFE Table Converter

This repository contains NASA's ELF to cFE Table Converter Tool (elf2cfetbl), which is a framework component of the Core Flight System.

This lab application is a ground utility to convert ELF to cFE binary tables for cFS. It is intended to be located in the `tools/elf2cfetbl` subdirectory of a cFS Mission Tree.  The Core Flight System is bundled at https://github.com/nasa/cFS (which includes this tool as a submodule), which includes build and execution instructions.

See README.txt for more information.

## Version Notes

- 3.1.1:
  - Minor updates (see https://github.com/nasa/elf2cfetbl/pull/19)
- 3.1.0:
  - Minor updates (see https://github.com/nasa/elf2cfetbl/pull/13)
  - Not backwards compatible with OSAL 4.2.1
- **3.0a OFFICIAL RELEASE**:
  - Released as part of cFE 6.6.0a under the Apache 2.0 license, see [LICENSE](LICENSE-18128-Apache-2_0.pdf).

NOTE - there are other parameter set management schemes used with the cFS (JSON, csv, etc) which may be more applicable for modern missions.  Contact the community as detailed below for more information.

## Known issues

This ground utility was developed for a specific mission/configuration, and may not be applicable for general use.  The Makefile and for_build/Makefile are no longer supported or tested.

## Getting Help

For best results, submit issues:questions or issues:help wanted requests at https://github.com/nasa/cFS.

Official cFS page: http://cfs.gsfc.nasa.gov

