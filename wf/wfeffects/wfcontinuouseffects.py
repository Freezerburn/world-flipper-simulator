from abc import ABC

from wf.wfenum import Element
from wf.wfeffects.wfeffect import WorldFlipperEffect


class AttackContinuousEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_attack"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.attack_modifier += self._calc_abil_lv()
        return True


class DirectDamageContinuousEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_direct_damage"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.stat_mod_da_damage += self._calc_abil_lv()
        return True


class SkillChargeRateContinuousEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_skill_gauge_chaging"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in self._only_mains(char_idxs):
            self.ctx.skill_charge_speed[idx] += self._calc_abil_lv()
        return True


class FireResistsContinuousEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_element_resistance"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.stat_mod_element_resists[Element.FIRE] += self._calc_abil_lv()
        return True


class IncreasedDirectHitsContinuousEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_aditional_direct_attack_and_damage"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.stat_mod_additional_da_damage += self._calc_abil_lv()
        self.ctx.stat_mod_additional_da_times = 2
        return True
