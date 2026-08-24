import struct
from packet import Packet, MessageType
from protocol.encoder import MAGIC, VERSION, HEADER_FORMAT, HEADER_NO_CRC_FORMAT, calculate_crc

HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def decode(data: bytes) -> Packet:
    if len(data) < HEADER_SIZE:
        raise ValueError("Packet too short")

    header_bytes = data[:HEADER_SIZE]

    magic, version, packet_type, flags, message_id, payload_length, crc = (
        struct.unpack(HEADER_FORMAT, header_bytes))

    payload = data[HEADER_SIZE : HEADER_SIZE + payload_length]

    header_without_crc = struct.pack(
        HEADER_NO_CRC_FORMAT,
        magic,
        version,
        packet_type,
        flags,
        message_id,
        payload_length
    )

    expected_crc = calculate_crc(header_without_crc + payload)

    if expected_crc != crc:
        raise ValueError("CRC mismatch")

    if magic != MAGIC:
        raise ValueError("Invalid magic")

    if version != VERSION:
        raise ValueError("Unsupported protocol version")

    if len(payload) != payload_length:
        raise ValueError("Incomplete payload")

    return Packet(
        packet_type=MessageType(packet_type),
        message_id=message_id,
        payload=payload,
        flags=flags
    )