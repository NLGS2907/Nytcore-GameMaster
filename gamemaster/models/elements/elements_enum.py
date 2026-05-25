from enum import IntEnum


class ElementType(IntEnum):
    """Element codes as they are presented in NIKKE."""

    WIND = 1
    WATER = 2
    IRON = 3
    FIRE = 4
    ELECTRIC = 5
