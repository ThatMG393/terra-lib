import ctypes
import struct
from typing import Literal


class BinaryReader:
    def __init__(self, binary: bytes, endian: Literal["little", "big"] = "little"):
        self.endian = endian
        self.binary = binary

        self.pointer = 0

    def ReadByte(self) -> int:
        tmp = self.binary[self.pointer]
        self.pointer = self.pointer + 1

        return tmp

    def ReadBoolean(self) -> bool:
        tmp = struct.unpack('?', self.binary[self.pointer:self.pointer + 1])[0]
        self.pointer = self.pointer + 1

        return tmp

    def ReadString(self, count: int = -1):
        """
        Read string from `self.pointer` to `count`
        Filters out non-printable character
        
        :return: a printable string
        """

        # Assumes that there is a byte that is the length of the string
        if count == -1:
            count = self.ReadByte()

        str_bytes = self.binary[self.pointer:self.pointer + count]
        dec_str = str_bytes.decode('utf-8', 'ignore')

        self.pointer = self.pointer + len(dec_str)
        return dec_str

    def ReadInt32(self) -> int:
        tmp = int.from_bytes(self.binary[self.pointer:self.pointer + 4], byteorder=self.endian)
        self.pointer = self.pointer + 4

        return tmp

    def ReadInt64(self) -> int:
        tmp = int.from_bytes(self.binary[self.pointer:self.pointer + 8], byteorder=self.endian)
        self.pointer = self.pointer + 8

        return tmp

    def ReadUInt32(self) -> int:
        tmp = int.from_bytes(self.binary[self.pointer:self.pointer + 4], byteorder=self.endian)
        tmp = ctypes.c_uint64(tmp).value
        self.pointer = self.pointer + 4

        return tmp

    def ReadULong64(self) -> int:
        tmp = int.from_bytes(self.binary[self.pointer:self.pointer + 8], byteorder=self.endian)
        self.pointer = self.pointer + 8

        return tmp

    # Only from .NET
    def ReadColor(self) -> tuple[int, int, int]:
        r = self.binary[self.pointer]
        self.pointer = self.pointer + 1

        g = self.binary[self.pointer]
        self.pointer = self.pointer + 1

        b = self.binary[self.pointer]
        self.pointer = self.pointer + 1

        return r, g, b

    def _MovePointer(self, pos: int):
        if pos > len(self.binary):
            pos = len(self.binary)
        elif pos < 0:
            pos = 0

        self.pointer = pos

    def _IncrementPointer(self, count: int):
        if pos > len(self.binary):
            pos = len(self.binary)
        elif pos < self.pointer:
            pos = self.pointer

        self.pointer = count


def bit_from_byte(byte: int, bit_index: int) -> int:
    return (byte >> bit_index) & 1
