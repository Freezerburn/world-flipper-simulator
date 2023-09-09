from __future__ import annotations
from typing import Type

from .wfcontinuousconditions import *
from .wfcontinuouseffects import *


continuous_condition_mapping: dict[str, Type[WorldFlipperCondition]] = {
    "0": HPAbovePercentContinuousCondition,
    "5": MultiballCountContinuousCondition,
    "8": BuffActiveContinuousCondition,
    "9": AttackBuffActiveContinuousCondition,
    "30": PierceActiveContinuousCondition,
    "37": AttackBuffsOnSelfContinuousCondition,
    "105": SkillGaugeAboveContinuousCondition,
    # NOTE: Condition is always hardcoded as Debuff.
    "134": DebuffsOnEnemyContinuousCondition,
}

continuous_effect_mapping: dict[str, list[Type[WorldFlipperEffect]]] = {
    "0": [AttackContinuousEffect],
    "1": [DirectDamageContinuousEffect],
    "3": [SkillChargeRateContinuousEffect],
    "5": [FireResistsContinuousEffect],
    # NOTE: Direct hits number (so far) is always hardcoded to 2.
    "45": [IncreasedDirectHitsContinuousEffect],
    "159": [DirectDamageContinuousEffect],
    "258": [AttackContinuousEffect],
}
