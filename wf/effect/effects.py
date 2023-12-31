from __future__ import annotations

from typing import Type
from abc import ABC

from wf.enum import CharPosition, Element, element_ab_to_enum
from wf.status_effect import StatusEffectKind
from wf.effect.base_effect import WorldFlipperBaseEffect


def NoOpMainEffect(ui_key: list[str]) -> Type[WorldFlipperBaseEffect]:
    class _NoOpMainEffect(WorldFlipperBaseEffect):
        @staticmethod
        def ui_key() -> list[str]:
            return ui_key

        def eval(self) -> bool:
            return False

        def _apply_effect(self, char_idxs: list[int]) -> bool:
            raise RuntimeError("Should never be called.")

    return _NoOpMainEffect


class ActiveForSecondsMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_for_second"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        return self._check_timed()


class AttackMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_attack"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if not self.is_target_main():
            return False
        self.ctx.attack_modifier += self._calc_abil_lv()
        return True


class DirectHitDamageMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_direct_damage"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if not self.is_target_main():
            return False
        self.ctx.stat_mod_da_damage += self._calc_abil_lv()
        return True


class SkillDamageMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_skill_damage"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.stat_mod_sd_damage += self._calc_abil_lv()
        return True


class PowerFlipDamageMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_power_flip_damage"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if not self.is_target_main():
            return False
        self.ctx.stat_mod_pf_damage += self._calc_abil_lv()
        return True


class FireResistDebuffSlayerMainEffect(WorldFlipperBaseEffect):
    """
    The underlying UI localization code has a parameter for what condition this effect is used with,
    but so far AHanabi is the only character that actually uses this effect and thus that parameter
    is effectively hard-coded to be for Fire Debuffs.
    """

    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(
                (StatusEffectKind.ELEMENT_RESIST, Element.FIRE)
            )
            self.ctx.condition_slayer += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class PoisonSlayerMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if not self.is_target_main():
            return False
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(StatusEffectKind.POISON)
            self.ctx.condition_slayer += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class PoisonAttackMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer_for_attack"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if not self.is_target_main():
            return False
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(StatusEffectKind.POISON)
            self.ctx.attack_modifier += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class PoisonDirectAttackMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer_for_direct_attack"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if not self.is_target_main():
            return False
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(StatusEffectKind.POISON)
            self.ctx.stat_mod_da_damage += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class SlowDebuffSlayerMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_slayer"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if self.state.enemy is None:
            return False
        try:
            self.state.enemy.debuffs.index(StatusEffectKind.SLOW)
            self.ctx.condition_slayer += self._calc_abil_lv()
            return True
        except ValueError:
            return False


class Lv3PowerFlipDamageMainEffect(WorldFlipperBaseEffect):
    """
    Technically the underlying UI localization code has a parameter for what level of Power Flip this
    is supposed to apply to. But in practice, every single character that has this effect ALWAYS
    uses Lv3 Power Flip.
    """

    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_power_flip_damage_lv"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.stat_mod_pf_lv_damage_slayer = self._calc_abil_lv()
        self.ctx.stat_mod_pf_lv_damage_slayer_lv = 3
        return True


class AttackBuffExtendMainEffect(WorldFlipperBaseEffect):
    """
    Technically this allows for any kind of condition to be passed in for time extension, but practically
    it's always hard-coded to be for Attack Buffs.
    """

    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_extend"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.attack_buff_extension += self._calc_abil_lv()
        return True


class PierceBuffExtendMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_condition_extend"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.pierce_buff_extension += self._calc_abil_lv()
        return True


class PowerFlipComboCountDownMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_power_flip_combo_count_down"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.pf_combo_reduction[2] += self._calc_abil_lv()
        return True


class IncreaseSkillChargeMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_content_skill_gauge"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in self._only_mains(char_idxs):
            self.ctx.skill_charge[idx] += self._calc_abil_lv()
        return True


class SkillChargeRateEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_skill_gauge_chaging"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in self._only_mains(char_idxs):
            self.ctx.skill_charge_speed[idx] += self._calc_abil_lv()
        return True


class SecondSkillGaugeMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_second_skill_gauge"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in self._only_mains(char_idxs):
            self.ctx.skill_gauge_max[idx] += 100
        return True


class InstantDamageMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_content_enemy_damage"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        return False


class PierceMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_content_enemy_damage"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if not self.is_target_main():
            return False
        self.ctx.pierce_active = True
        return True


class FeverGainRateMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_fever_point"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        if not self.is_target_main():
            return False
        self.ctx.fever_gain_from_attacks += self._calc_abil_lv()
        return True


class FireResistEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_element_resistance"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.stat_mod_element_resists[Element.FIRE] += self._calc_abil_lv()
        return True


class IncreaseHpMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_content_hp"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in self._only_mains(char_idxs):
            self.ctx.increased_hp[idx] += self._calc_abil_lv()
        return True


class IncreaseComboMainEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_condition_content_combo_boost"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.combo += self._calc_abil_lv()
        return True


class IncreasedDirectHitsEffect(WorldFlipperBaseEffect):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_common_content_aditional_direct_attack_and_damage"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.ctx.stat_mod_additional_da_damage += self._calc_abil_lv()
        self.ctx.stat_mod_additional_da_times = 2
        return True
