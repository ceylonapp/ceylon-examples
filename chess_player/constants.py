import enum


class Error(enum.Enum):
    INVALID_MOVE = 500
    NOT_STARTED = 501


class Status(enum.Enum):
    ACT = 400
    CHECK = 401
    CHECK_MATE = 402
    ATTACK = 403
