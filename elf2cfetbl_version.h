/*
**  GSC-18128-1, "Core Flight Executive Version 6.7"
**
**  Copyright (c) 2006-2019 United States Government as represented by
**  the Administrator of the National Aeronautics and Space Administration.
**  All Rights Reserved.
**
**  Licensed under the Apache License, Version 2.0 (the "License");
**  you may not use this file except in compliance with the License.
**  You may obtain a copy of the License at
**
**    http://www.apache.org/licenses/LICENSE-2.0
**
**  Unless required by applicable law or agreed to in writing, software
**  distributed under the License is distributed on an "AS IS" BASIS,
**  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
**  See the License for the specific language governing permissions and
**  limitations under the License.
*/

/*
 *  File: elf2cfetbl_version.h
 *
 *  Purpose:
 *  Provide version identifiers for the ELF to cFE Table Converter.
 *  See cfe documentation for version and build number and description
 */

#ifndef ELF2CFETBL_VERSION_H
#define ELF2CFETBL_VERSION_H


/* Development Build Macro Definitions */
/** @brief Number of commits since baseline v3.1.0 */
#define ELF2CFETBL_BUILD_NUMBER 36 
#define ELF2CFETBL_BUILD_BASELINE "v3.1.0+dev"

/*
 * Version Macro Definitions
 * These are only used for OFFICIAL release builds.
 */
#define ELF2CFETBL_MAJOR_VERSION 3
#define ELF2CFETBL_MINOR_VERSION 1
#define ELF2CFETBL_REVISION      0
#define ELF2CFETBL_MISSION_REV   0

/*
 * Tools to construct version string
 */
#define ELF2CFETBL_STR_HELPER(x) #x
#define ELF2CFETBL_STR(x)        ELF2CFETBL_STR_HELPER(x)

/* Development Build Format for ELF2CFETBL_VERSION */
/* Baseling git tag + Number of commits since baseline, see elf2cfetbl_buildnumber.h */ 
#define ELF2CFETBL_VERSION ELF2CFETBL_BUILD_BASELINE ELF2CFETBL_STR(ELF2CFETBL_BUILD_NUMBER)

/* Development Build Format for ELF2CFETBL_VERSION_STRING */
#define ELF2CFETBL_VERSION_STRING                                                         \
    " elf2cfetbl Development Build\n"                                                     \
    " " ELF2CFETBL_VERSION " (Codename: Bootes)\n" /* Codename for current development */ \
    " Last Offical Release: elf2cfetbl v3.1.0"     /* For full support please use official release version */

/* Use the following templates for Official Releases ONLY */
  /* Official Release format for ELF2CFETBL_VERSION */
  /* 
    #define ELF2CFETBL_VERSION "v"               \    
    ELF2CFETBL_STR(ELF2CFETBL_MAJOR_VERSION) "." \
    ELF2CFETBL_STR(ELF2CFETBL_MINOR_VERSION) "." \
    ELF2CFETBL_STR(ELF2CFETBL_REVISION) "."      \
    ELF2CFETBL_STR(ELF2CFETBL_MISSION_REV)         
  */
  
  
  /* Official Release format for ELF2CFETBL_VERSION_STRING */
  /*
    #define ELF2CFETBL_VERSION_STRING "elf2cfetbl " ELF2CFETBL_VERSION
  */
  
/* END TEMPLATES */


#endif /* ELF2CFETBL_VERSION_H */
