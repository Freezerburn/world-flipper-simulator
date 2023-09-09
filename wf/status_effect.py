from enum import StrEnum, auto
from typing import cast

from typing_extensions import TypedDict

from .enum import Element


class StatusEffectKind(StrEnum):
    ATTACK = auto()
    HP = auto()
    DIRECT_ATTACK_DAMAGE = auto()
    POWER_FLIP_DAMAGE = auto()
    SKILL_DAMAGE = auto()
    ABILITY_DAMAGE = auto()
    ELEMENT_RESIST = auto()
    DIRECT_ATTACK_RESIST = auto()
    POWER_FLIP_RESIST = auto()
    SKILL_DAMAGE_RESIST = auto()
    ABILITY_DAMAGE_RESIST = auto()
    DAMAGE_CUT = auto()
    REGENERATION = auto()
    POISON = auto()
    PARALYSIS = auto()
    STUN = auto()
    SLOW = auto()
    LETHARGY = auto()
    SILENCE = auto()
    FEVER_GAUGE = auto()
    DOWN_GAUGE = auto()
    DEBUFF_IMMUNITY = auto()
    MULTI_HIT = auto()
    PIERCE = auto()
    FLOAT = auto()
    SPEED_UP = auto()
    ADVERSITY = auto()
    COMBO_UP = auto()
    GUTS = auto()
    BIPOLAR = auto()


class StatusEffectKwargs(TypedDict, total=False):
    percent_mod: float
    element: Element
    combo: int


class StatusEffect:
    def __init__(
        self, kind: StatusEffectKind, time_start: int, time_active: int, **kwargs
    ):
        typed_kwargs = cast(StatusEffectKwargs, kwargs)
        self.kind = kind
        self.time_start = time_start
        self.time_active = time_active
        self.percent_mod = typed_kwargs.get("percent_mod")
        self.element = typed_kwargs.get("element")
        self.combo = typed_kwargs.get("combo")

    def __eq__(self, other):
        if isinstance(other, StatusEffect):
            return (
                self.kind == other.kind
                and self.time_start == other.time_start
                and self.time_active == other.time_active
                and self.percent_mod == other.percent_mod
                and self.element == other.element
                and self.combo == other.combo
            )
        elif isinstance(other, StatusEffectKind):
            return self.kind == other
        elif isinstance(other, tuple):
            if isinstance(other[0], StatusEffectKind) and isinstance(other[1], Element):
                return self.kind == other[0] and self.element == other[1]
        return False
