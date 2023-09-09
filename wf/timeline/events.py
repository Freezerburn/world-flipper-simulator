from __future__ import annotations
from typing import Literal
from enum import Enum, auto


class EventKind(Enum):
    BALL_FLIP = auto()
    POWER_FLIP = auto()
    COMBO_REACHED = auto()
    SKILL_ACTIVATED = auto()
    SKILL_CHARGE_ADD = auto()
    SKILL_CHARGE_100 = auto()
    ABILITY_ACTIVATED = auto()
    TOOK_DAMAGE = auto()
    FEVER_START = auto()
    FEVER_END = auto()

    DIRECT_HIT = auto()
    POWER_FLIP_HIT = auto()
    SKILL_HIT = auto()
    ABILITY_HIT = auto()

    GAINED_BARRIER = auto()
    GAINED_BUFF = auto()
    GAINED_DEBUFF = auto()

    PIERCE_ACTIVATED = auto()
    FLOAT_ACTIVATED = auto()
    PIERCE_DEACTIVATED = auto()
    FLOAT_DEACTIVATED = auto()


class Event:
    def __init__(self, kind: EventKind):
        self.time_activated: int = 0
        self.kind: EventKind = kind

        self.powerflip_level: Literal[-1, 1, 2, 3] = -1
        self.combo: int = -1
        self.skill_unit: Literal[-1, 0, 1, 2] = -1
        self.ability: Literal[-1, 0, 1, 2, 3, 4, 5] = -1
        self.direct_hits: int = -1
        self.power_flip_hits: int = -1
        self.skill_hits: int = -1
