from enum import Enum


class CallType(str, Enum):
    INCOMING = "INCOMING"
    OUTGOING = "OUTGOING"
