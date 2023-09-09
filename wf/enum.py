from enum import StrEnum, auto
from typing import Optional, Literal


class Element(StrEnum):
    ANY = auto()
    NONE = auto()

    FIRE = auto()
    WATER = auto()
    THUNDER = auto()
    WIND = auto()
    DARK = auto()
    LIGHT = auto()


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

    def is_main(self) -> bool:
        return self == CharPosition.LEADER or self == CharPosition.MAIN


class EffectType(StrEnum):
    MAIN_CONDITION = auto()
    MAIN_EFFECT = auto()
    CONTINUOUS_CONDITION = auto()
    CONTINOUS_EFFECT = auto()


AbilityElementType = Literal["Red", "Yellow", "Green", "Blue", "White", "Black"]


def element_ab_to_enum(element: AbilityElementType) -> Optional[Element]:
    match element:
        case "Red":
            return Element.FIRE
        case "Yellow":
            return Element.THUNDER
        case "Green":
            return Element.WIND
        case "Blue":
            return Element.WATER
        case "White":
            return Element.LIGHT
        case "Black":
            return Element.DARK
        case _:
            return None
