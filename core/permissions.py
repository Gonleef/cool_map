from enum import IntFlag


class Permissions(IntFlag):
    Null = 0
    Auth = 1

    Api = Auth | 1 << 1
    Create = Auth | 1 << 2

    Read = Auth | 1 << 10
    Write = Auth | 1 << 11
