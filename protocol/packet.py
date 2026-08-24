from dataclasses import dataclass
from enum import IntEnum


class MessageType(IntEnum):
    TEXT = 0x01
    PING = 0x02
    PONG = 0x03
    ACK = 0x04
    ERROR = 0x05


@dataclass
class Packet:
    packet_type: MessageType
    message_id: int
    payload: bytes
    flags: int = 0