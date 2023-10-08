from __future__ import annotations

from .effects import *
from .conditions import *


continuous_condition_mapping: dict[str, Type[WorldFlipperBaseCondition]] = {
    "0": HPAbovePercentCondition,
    "5": MultiballCountCondition,
    "8": BuffActiveCondition,
    "9": AttackBuffActiveCondition,
    "30": PierceActiveCondition,
    "37": AttackBuffsOnSelfCondition,
    "105": SkillGaugeAboveCondition,
    # NOTE: Condition is always hardcoded as Debuff.
    "134": DebuffsOnEnemyCondition,
}

continuous_effect_mapping: dict[str, list[Type[WorldFlipperBaseEffect]]] = {
    "0": [AttackMainEffect],
    "1": [DirectHitDamageMainEffect],
    "3": [SkillChargeRateEffect],
    "5": [FireResistEffect],
    # NOTE: Direct hits number (so far) is always hardcoded to 2.
    "45": [IncreasedDirectHitsEffect],
    "159": [DirectHitDamageMainEffect],
    "258": [AttackMainEffect],
}
