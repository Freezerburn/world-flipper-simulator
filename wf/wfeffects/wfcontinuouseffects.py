from abc import ABC

from wf.wfenum import Element
from wf.wfeffects.wfeffect import WorldFlipperCondition


class WorldFlipperContinuousEffect(WorldFlipperCondition, ABC):
    def _calc_abil_lv(self) -> int:
        v_min = int(self.ability.continuous_effect_min) / 100_000
        v_max = int(self.ability.continuous_effect_max) / 100_000
        step = abs(v_max - v_min) / 5
        return (v_min + step * (self.lv - 1)) * self.multiplier


class AttackContinuousEffect(WorldFlipperContinuousEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_attack"]

    def eval(self) -> bool:
        self.ctx.attack_modifier += self._calc_abil_lv()
        return True


class DirectDamageContinuousEffect(WorldFlipperContinuousEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_direct_damage"]

    def eval(self) -> bool:
        self.ctx.stat_mod_da_damage += self._calc_abil_lv()
        return True


class SkillChargeRateContinuousEffect(WorldFlipperContinuousEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_skill_gauge_chaging"]

    def eval(self) -> bool:
        self.ctx.skill_charge_speed[self.eval_char_idx] += self._calc_abil_lv()
        return True


class FireResistsContinuousEffect(WorldFlipperContinuousEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_element_resistance"]

    def eval(self) -> bool:
        self.ctx.stat_mod_element_resists[Element.FIRE] += self._calc_abil_lv()
        return True


class IncreasedDirectHitsContinuousEffect(WorldFlipperContinuousEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_aditional_direct_attack_and_damage"]

    def eval(self) -> bool:
        self.ctx.stat_mod_additional_da_damage += self._calc_abil_lv()
        self.ctx.stat_mod_additional_da_times = 2
        return True
