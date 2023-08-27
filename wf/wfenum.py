from enum import StrEnum, auto


class Element(StrEnum):
    ANY = auto()

    FIRE = auto()
    WATER = auto()
    THUNDER = auto()
    WIND = auto()
    DARK = auto()
    LIGHT = auto()


class Buff(StrEnum):
    ATTACK = auto()
    HP = auto()
    POWER_FLIP = auto()
    SKILL_DAMAGE = auto()


class PowerFlip(StrEnum):
    SWORD = auto()
    BOW = auto()
    FIST = auto()
    SPECIAL = auto()
    SUPPORT = auto()


class CharPosition(StrEnum):
    LEADER = auto()
    MAIN = auto()
    UNISON = auto()