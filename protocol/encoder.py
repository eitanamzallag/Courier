import struct
from packet import Packet, MessageType
import zlib

MAGIC = 0xDEC0DE
VERSION = 0x01
HEADER_NO_CRC_FORMAT = "!IBBBII"
HEADER_FORMAT = "!IBBBIII"

def calculate_crc(data: bytes) -> int:
    return zlib.crc32(data) & 0xffffffff

def encode(packet: Packet) -> bytes:
    payload_length = len(packet.payload)
    header_without_crc = struct.pack(HEADER_NO_CRC_FORMAT,
                                     MAGIC, VERSION, packet.packet_type,
                                     packet.flags, packet.message_id, payload_length)

    crc = calculate_crc(header_without_crc + packet.payload)

    header = struct.pack(HEADER_FORMAT, MAGIC, VERSION, packet.packet_type,
                                     packet.flags, packet.message_id, payload_length, crc)



    return header + packet.payload