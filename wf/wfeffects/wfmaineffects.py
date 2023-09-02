from __future__ import annotations

from typing import Type
from abc import ABC

from wf.wfenum import CharPosition, Debuff, Element, element_ab_to_enum
from wf.wfeffects.wfeffect import WorldFlipperEffect


def NoOpMainEffect(ui_key: list[str]) -> Type[WorldFlipperEffect]:
    class _NoOpMainEffect(WorldFlipperEffect):
        @staticmethod
        def ui_key() -> list[str]:
            return ui_key

        def eval(self) -> bool:
            return False

    return _NoOpMainEffect


class ActiveForSecondsMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_for_second"]

    def eval(self) -> bool:
        return self.state.ability_condition_active[self.ability_char_idx][
            self.ability_idx
        ]


class AttackMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_attack"]

    def eval(self) -> bool:
        if not self.is_target_main():
            return False
        self.ctx.attack_modifier += self._calc_abil_lv()
        return True


class SkillDamageMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_skill_damage"]

    def eval(self) -> bool:
        self.ctx.stat_mod_sd_damage += self._calc_abil_lv()
        return True


class PowerFlipDamageMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_power_flip_damage"]

    def eval(self) -> bool:
        if self.eval_char_position != CharPosition.LEADER:
            return False
        self.ctx.stat_mod_pf_damage += self._calc_abil_lv()
        return True


class FireResistDebuffSlayerMainEffect(WorldFlipperEffect):
    """
    The underlying UI localization code has a parameter for what condition this effect is used with,
    but so far AHanabi is the only character that actually uses this effect and thus that parameter
    is effectively hard-coded to be for Fire Debuffs.
    """

    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer"]

    def eval(self) -> bool:
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(Debuff.FIRE_RESISTANCE)
            self.ctx.condition_slayer += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class PoisonSlayerMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer"]

    def eval(self) -> bool:
        if not self.is_target_main():
            return False
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(Debuff.POISON)
            self.ctx.condition_slayer += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class PoisonAttackMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer_for_attack"]

    def eval(self) -> bool:
        if not self.is_target_main():
            return False
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(Debuff.POISON)
            self.ctx.attack_modifier += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class PoisonDirectAttackMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer_for_direct_attack"]

    def eval(self) -> bool:
        if not self.is_target_main():
            return False
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(Debuff.POISON)
            self.ctx.stat_mod_da_damage += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class SlowDebuffSlayerMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer"]

    def eval(self) -> bool:
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(Debuff.SLOW)
            self.ctx.condition_slayer += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class Lv3PowerFlipDamageMainEffect(WorldFlipperEffect):
    """
    Technically the underlying UI localization code has a parameter for what level of Power Flip this
    is supposed to apply to. But in practice, every single character that has this effect ALWAYS
    uses Lv3 Power Flip.
    """

    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_power_flip_damage_lv"]

    def eval(self) -> bool:
        self.ctx.stat_mod_pf_lv_damage_slayer = self._calc_abil_lv()
        self.ctx.stat_mod_pf_lv_damage_slayer_lv = 3
        return True


class AttackBuffExtendMainEffect(WorldFlipperEffect):
    """
    Technically this allows for any kind of condition to be passed in for time extension, but practically
    it's always hard-coded to be for Attack Buffs.
    """

    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_extend"]

    def eval(self) -> bool:
        self.ctx.attack_buff_extension += self._calc_abil_lv()
        return True


class PowerFlipComboCountDownMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_power_flip_combo_count_down"]

    def eval(self) -> bool:
        self.ctx.pf_combo_reduction[2] += self._calc_abil_lv()
        return True


class IncreaseSkillChargeMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_content_skill_gauge"]

    def eval(self) -> bool:
        self.ctx.skill_charge[
            self.state.main_index(self.eval_char_idx)
        ] += self._calc_abil_lv()
        return True


class SecondSkillGaugeMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_second_skill_gauge"]

    def eval(self) -> bool:
        self.ctx.skill_gauge_max[self.state.main_index(self.eval_char_idx)] += 100
        return True


class InstantDamageMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_content_enemy_damage"]

    def eval(self) -> bool:
        return False


class PierceMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_content_enemy_damage"]

    def eval(self) -> bool:
        if not self.is_target_main():
            return False
        self.ctx.pierce_active = True
        return True


class FeverGainRateMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_fever_point"]

    def eval(self) -> bool:
        if not self.is_target_main():
            return False
        self.ctx.fever_gain_from_attacks += self._calc_abil_lv()
        return True


class ResistUpMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_element_resistance"]

    def eval(self) -> bool:
        element = element_ab_to_enum(self.ability.main_effect_element)
        if self.eval_char.element != element:
            return False
        self.ctx.stat_mod_element_resists[Element.FIRE] += self._calc_abil_lv()
        return True


class IncreaseHpMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_content_hp"]

    def eval(self) -> bool:
        self.ctx.increased_hp[self.eval_char_idx] += self._calc_abil_lv()
        return True


class IncreaseComboMainEffect(WorldFlipperEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_condition_content_combo_boost"]

    def eval(self) -> bool:
        self.ctx.combo += self._calc_abil_lv()
        return True
