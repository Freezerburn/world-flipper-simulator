from __future__ import annotations
from typing import Literal
from enum import Enum, auto


class EventKind(Enum):
    BALL_FLIP = auto()
    POWER_FLIP = auto()
    COMBO_REACHED = auto()
    SKILL_ACTIVATED = auto()
    ABILITY_ACTIVATED = auto()
    DIRECT_HIT = auto()
    POWER_FLIP_HIT = auto()
    SKILL_HIT = auto()


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
