import ctypes
import string
from typing import Literal


class BinaryReader:
    def __init__(self, binary: bytes, endian: Literal["little", "big"] = "little"):
        self.endian = endian
        self.binary = binary

        self.pointer = 0

    def ReadByte(self) -> int:
        return self.binary[self.pointer]

    def ReadString(self, count: int):
        str_bytes = self.binary[self.pointer:self.pointer + count]

        tmp = str_bytes.decode('utf-8', 'ignore')
        dec_str = ""

        i = 0
        while i < len(tmp):
            if tmp[i] not in string.printable:
                i += 1
                continue
            if i + 1 < len(tmp) and tmp[i + 1] in string.printable:
                dec_str += tmp[i]
                i += 1
            else:
                dec_str += tmp[i]
                break

        self.pointer = self.pointer + len(dec_str)
        return dec_str

    def ReadStringInternal(self) -> str:
        cur_pos = 0
        n = 0
        str_len = 0
        read_len = 0
        chars_read = 0

        char_buffer = bytes(128)
        char_bytes = bytes(len(char_buffer))

        str_len = self._Read7BitEncodedInt()
        if str_len < 0:
            return 'h'

        while cur_pos < str_len:
            read_len = str_len - cur_pos  # TODO: clamp
            cur_pos = cur_pos + 1

    def ReadInt32(self) -> int:
        tmp = int.from_bytes(self.binary[self.pointer:self.pointer + 4], byteorder=self.endian)
        self.pointer = self.pointer + 4

        return tmp

    def ReadUInt64(self) -> int:
        tmp = int.from_bytes(self.binary[self.pointer:self.pointer + 4], byteorder=self.endian)
        tmp = ctypes.c_uint64(tmp).value
        self.pointer = self.pointer + 4

        return tmp

    def ReadULong64(self) -> int:
        tmp = int.from_bytes(self.binary[self.pointer:self.pointer + 8], byteorder=self.endian)
        self.pointer = self.pointer + 8

        return tmp

    def _Read7BitEncodedInt(self) -> int:
        count = 0
        shift = 0
        byte = 0

        while (byte & 0x80) != 0:
            if shift == 5 * 7:
                break

            byte = self.ReadByte()
            count = count | (byte & 0x7F) << shift
            shift = shift + 7

        return count

    def _MovePointer(self, pos: int):
        if pos > len(self.binary):
            pos = len(self.binary)
        elif pos < 0:
            pos = 0

        self.pointer = pos
