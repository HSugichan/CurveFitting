from enum import IntEnum, auto


class ErrorCode(IntEnum):
    Success = 0
    InvalidArgs = auto()
    MissingParameter = auto()
    NoContents = auto()
    UnfoundFile = auto()
    Unexpected = 999
