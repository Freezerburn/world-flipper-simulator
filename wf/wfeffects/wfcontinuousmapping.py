from __future__ import annotations
from typing import Type

from .wfcontinuousconditions import *
from .wfcontinuouseffects import *


continuous_condition_mapping: dict[str, Type[WorldFlipperContinuousCondition]] = {
    "5": MultiballCountContinuousCondition,
    "8": BuffActiveContinuousCondition,
    "105": SkillGaugeAboveContinuousCondition,
    # NOTE: Condition is always hardcoded as Debuff.
    "134": DebuffsOnEnemyContinuousCondition,
}

continuous_effect_mapping: dict[str, list[Type[WorldFlipperContinuousEffect]]] = {
    "0": [AttackContinuousEffect],
    "3": [SkillChargeRateContinuousEffect],
    # NOTE: Direct hits number (so far) is always hardcoded to 2.
    "45": [IncreasedDirectHitsContinuousEffect],
    "159": [DirectDamageContinuousEffect],
    "258": [AttackContinuousEffect],
}