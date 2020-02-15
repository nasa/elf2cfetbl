import lief

from collections import namedtuple
from enum import Enum
import os
import sys

# Constants
TBL_DEF_SYMBOL_NAME = "CFE_TBL_FileDef"
OBJECT_NAME_LEN = 64
CFE_MISSION_TBL_MAX_FULL_NAME_LEN = 40
CFE_FS_HDR_DESC_MAX_LEN = 32
CFE_MISSION_MAX_FILE_LEN = 20

HEADER_MAGIC_NUMBER = 0x63464531
CFE_FS_SubType_TBL_IMG = 8
SIZE_CFE_FS_Header_t = 64

DEFAULT_SPACECRAFT_ID = 0  # via args
DEFAULT_PROCESSOR_ID = 0  # via args
DEFAULT_APPLICATION_ID = 0  # via args
DEFAULT_SECONDS = 0  # via args
DEFAULT_SUBSECONDS = 0  # via args

UNUSED_ZERO = 0

CFE_TBL_FileDef_t = namedtuple("CFE_TBL_FileDef_t", "object_name table_name description tgt_file_name object_size")


def dump_tbl_def(tbl_def):
    print("Table Defined as follows:")
    print("   Data Object: {}".format(tbl_def.object_name))
    print("   Table Name : '{}'".format(tbl_def.table_name))
    print("   Description: '{}'".format(tbl_def.description))
    print("   Output File: {}".format(tbl_def.tgt_file_name))

    object_size_hex = "0x%0.8X" % tbl_def.object_size
    print("   Object Size: {} ({})".format(tbl_def.object_size, object_size_hex))


TableDefinition = namedtuple("TableDefinition", "metadata content")


class BinaryFormat(Enum):
    ELF = 1
    MACHO = 2


def byte_array_to_string(byte_array):
    return bytes(byte_array).decode('utf-8').replace('\x00', '')


class TableDefReader:
    def get_tbl_def_info(self, input_path):
        binary_format = self.detect_binary_format(input_path)

        input_file = lief.parse(input_path)

        tbl_def_symbol = self.find_symbol(input_file, binary_format, TBL_DEF_SYMBOL_NAME)
        assert tbl_def_symbol

        tbl_filedef_section = self.find_tbl_def_section(input_file, binary_format, tbl_def_symbol)
        assert tbl_filedef_section

        tbl_def = self.read_tbl_def_from_section(tbl_filedef_section, tbl_def_symbol)
        dump_tbl_def(tbl_def)

        object_symbol = self.find_symbol(input_file, binary_format, tbl_def.object_name)
        assert object_symbol

        content = tbl_filedef_section.content[object_symbol.value:tbl_def.object_size]

        return TableDefinition(metadata=tbl_def, content=content)

    @staticmethod
    def detect_binary_format(input_path):
        if lief.is_macho(input_path):
            return BinaryFormat.MACHO
        elif lief.is_elf(input_path):
            return BinaryFormat.ELF
        else:
            return None

    @staticmethod
    def read_tbl_def_from_section(tbl_filedef_section, tbl_def_symbol):
        print("tbl_filedef_section.content: {}".format(tbl_filedef_section.content))
        tbl_filedef_offset = tbl_def_symbol.value
        object_name = tbl_filedef_section.content[tbl_filedef_offset:tbl_filedef_offset + OBJECT_NAME_LEN]
        object_name_string = byte_array_to_string(object_name)
        print(object_name_string)
        assert len(object_name) == OBJECT_NAME_LEN

        tbl_filedef_offset += OBJECT_NAME_LEN
        table_name = tbl_filedef_section.content[
                     tbl_filedef_offset:tbl_filedef_offset + CFE_MISSION_TBL_MAX_FULL_NAME_LEN]
        assert len(table_name) == CFE_MISSION_TBL_MAX_FULL_NAME_LEN
        table_name_string = byte_array_to_string(table_name)

        tbl_filedef_offset += CFE_MISSION_TBL_MAX_FULL_NAME_LEN
        description = tbl_filedef_section.content[tbl_filedef_offset:tbl_filedef_offset + CFE_FS_HDR_DESC_MAX_LEN]
        assert len(description) == CFE_FS_HDR_DESC_MAX_LEN
        description_string = byte_array_to_string(description)

        tbl_filedef_offset += CFE_FS_HDR_DESC_MAX_LEN
        target_file_name = tbl_filedef_section.content[tbl_filedef_offset:tbl_filedef_offset + CFE_MISSION_MAX_FILE_LEN]
        assert len(target_file_name) == CFE_MISSION_MAX_FILE_LEN
        target_file_name_string = byte_array_to_string(target_file_name)

        tbl_filedef_offset += CFE_MISSION_MAX_FILE_LEN
        object_size_bytes = tbl_filedef_section.content[tbl_filedef_offset:tbl_filedef_offset + 4]
        assert len(object_size_bytes) == 4
        object_size = int.from_bytes(object_size_bytes, "little")

        return CFE_TBL_FileDef_t(object_name=object_name_string,
                                 table_name=table_name_string,
                                 description=description_string,
                                 tgt_file_name=target_file_name_string,
                                 object_size=object_size)

    @staticmethod
    def find_tbl_def_section(input_file, binary_format, tbl_def_symbol):
        if binary_format == BinaryFormat.MACHO:
            tbl_def_section = input_file.get_section("__data")
        else:
            tbl_def_section = input_file.sections[tbl_def_symbol.shndx]
        assert tbl_def_section
        return tbl_def_section

    @staticmethod
    def find_symbol(input_file, binary_format, symbol_name):
        if binary_format == BinaryFormat.ELF:
            return input_file.get_symbol(symbol_name)
        elif binary_format == BinaryFormat.MACHO:
            mangled_symbol_name = "_{}".format(symbol_name)
            return input_file.get_symbol(mangled_symbol_name)
        else:
            assert 0, "Unsupported format: ".format(binary_format)


class TableDefWriter:
    @staticmethod
    def write(output_path, table_definition):
        table_definition_content = table_definition.content
        table_definition_metadata = table_definition.metadata

        print("object_symbol_content: {}".format(table_definition_content))

        file_header_content_type = (HEADER_MAGIC_NUMBER).to_bytes(4, "big")
        file_header_sub_type = (CFE_FS_SubType_TBL_IMG).to_bytes(4, "big")
        file_header_length = (SIZE_CFE_FS_Header_t).to_bytes(4, "big")
        file_header_spacecraft_id = (DEFAULT_SPACECRAFT_ID).to_bytes(4, "big")
        file_header_processor_id = (DEFAULT_PROCESSOR_ID).to_bytes(4, "big")
        file_header_application_id = (DEFAULT_APPLICATION_ID).to_bytes(4, "big")
        file_header_time_seconds = (DEFAULT_SECONDS).to_bytes(4, "big")
        file_header_time_sub_seconds = (DEFAULT_SUBSECONDS).to_bytes(4, "big")

        file_header_description = table_definition_metadata.description.ljust(CFE_FS_HDR_DESC_MAX_LEN, '\x00').encode()
        print(file_header_description)
        file_header_reserved = (UNUSED_ZERO).to_bytes(4, "big")
        file_header_offset = (UNUSED_ZERO).to_bytes(4, "big")

        # assert object_size == 4
        file_header_num_bytes = table_definition_metadata.object_size.to_bytes(4, "big")

        file_header_table_names = table_definition_metadata.table_name.ljust(CFE_MISSION_TBL_MAX_FULL_NAME_LEN,
                                                                             '\x00').encode()
        assert len(file_header_table_names) == 40

        outfile = open(output_path, 'wb')

        outfile.write(file_header_content_type)
        outfile.write(file_header_sub_type)
        outfile.write(file_header_length)
        outfile.write(file_header_spacecraft_id)
        outfile.write(file_header_processor_id)
        outfile.write(file_header_application_id)
        outfile.write(file_header_time_seconds)
        outfile.write(file_header_time_sub_seconds)
        outfile.write(file_header_description)
        outfile.write(file_header_reserved)
        outfile.write(file_header_offset)
        outfile.write(file_header_num_bytes)
        outfile.write(file_header_table_names)

        # TODO: if TableDataIsAllZeros case
        outfile.write(bytes(table_definition_content))


def main(argv):
    if len(argv) != 3:
        print("error: two arguments must be provided: input file path and output file path")
        exit(2)

    input_path = argv[1]
    if not os.path.exists(input_path):
        print("error: file does not exist: {}".format(input_path))
        exit(2)

    output_path = argv[2]

    # TODO
    print("Original Source File Modification Time: TODO TODO TODO")

    table_def_reader = TableDefReader()

    table_definition = table_def_reader.get_tbl_def_info(input_path)

    table_def_writer = TableDefWriter()
    table_def_writer.write(output_path, table_definition)


main(sys.argv)
