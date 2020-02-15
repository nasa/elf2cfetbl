set(LIT_EXEC lit)
set(FILECHECK_EXEC filecheck)

set(LIT_COMMAND
  ELF2TBL_EXEC=$<TARGET_FILE:elf2cfetbl>
  BIN2TBL_EXEC=${CMAKE_CURRENT_SOURCE_DIR}/bin2cfetbl/bin2cfetbl.py
  FILECHECK_EXEC=${FILECHECK_EXEC}
  ${LIT_EXEC}
  -vv
  ${CMAKE_CURRENT_SOURCE_DIR}/tests
)

add_custom_target(bin2cfetbl-tests-integration
  DEPENDS elf2cfetbl
)

add_custom_command(
  TARGET bin2cfetbl-tests-integration
  COMMAND ${LIT_COMMAND}
)
