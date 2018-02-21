from enum import IntFlag


class Permissions(IntFlag):
    Null = 0xFF
    Auth = 0xFE

    Use = 1 << 0
