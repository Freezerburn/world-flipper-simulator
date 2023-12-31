from __future__ import annotations

from typing import Type
import math

from wf.enum import element_ab_to_enum
from wf.effect.base_effect import WorldFlipperBaseCondition
from wf.party import main_index, mains_only_index
from wf.status_effect import StatusEffectKind


class OnBattleStartMainCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_first_flip"]

    def eval(self) -> bool:
        return True

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        raise RuntimeError("Should never be called.")


def NTimesCondition(following_ui_name: str) -> Type[WorldFlipperBaseCondition]:
    class _NTimesCondition(WorldFlipperBaseCondition):
        @staticmethod
        def ui_key() -> list[str]:
            return ["ability_description_n_times"]

        def _apply_effect(self, char_idxs: list[int]) -> bool:
            match following_ui_name:
                case "ability_description_instant_trigger_kind_power_flip":
                    self.multiplier = self._calc_multiplier(
                        int(self.ability.main_effect_max_multiplier),
                        self.state.total_powerflips,
                    )

                case "ability_description_instant_trigger_kind_skill_hit":
                    self.multiplier = self._calc_multiplier(
                        int(self.ability.main_effect_max_multiplier),
                        self.state.skill_hits[self.ability_char_idx],
                    )

                case "ability_description_instant_trigger_kind_ball_flip":
                    self.multiplier = self._calc_multiplier(
                        int(self.ability.main_effect_max_multiplier),
                        self.state.total_ball_flips,
                    )

                case _:
                    raise RuntimeError(
                        f"[{self.ability.name}] Failed to eval secondary condition: {self.ui_name[1]}"
                    )
            return True

    return _NTimesCondition


class OnSkillInvokeMainCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_skill_invoke"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        activations_per_effect = self._calc_abil_lv()
        self.multiplier = 0
        for idx in char_idxs:
            self.multiplier += (
                self.state.skill_activations[idx] / activations_per_effect
            )
        # There are effect types that don't care about multipliers. An example of this is
        # AHanabi's ability 2, which deals damage to all units when a skill is activated with
        # a cooldown on how often this can occur.
        if self.ability.main_effect_max_multiplier == "(None)":
            max_mult = 9999
        else:
            max_mult = int(self.ability.main_effect_max_multiplier)
        if self.multiplier > max_mult:
            self.multiplier = max_mult
        return True


class OnSkillGaugeReach100MainCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_skill_max"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.multiplier = 0
        # Calling code has no idea that we might need to limit the indexes to just the main unit ones.
        # So we guard against the possibility of being handed, as an example, every unit in the party.
        # We also need to avoid double-counting any individual set of units in the party.
        main_idxs: set[int] = set()
        for idx in char_idxs:
            main_idxs.add(main_index(idx))
        for idx in main_idxs:
            self.multiplier += self._calc_multiplier(
                int(self.ability.main_effect_max_multiplier),
                self.state.times_skill_reached_100[idx],
            )
        return True


class PartyMembersAddedMainCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_member"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.multiplier = self._calc_multiplier(
            int(self.ability.main_effect_max_multiplier),
            len(char_idxs),
        )
        return True


class Lv3PowerFlipsMainCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_power_flip_lv"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.multiplier = self._calc_multiplier(
            int(self.ability.main_effect_max_multiplier),
            self.state.powerflips_by_lv[2],
        )
        return True


class ComboReachedMainCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_combo"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        combo_req = self._calc_abil_lv()
        num_combos = self.state.combos_reached.get(combo_req, 0)
        max_combos = int(self.ability.main_effect_max_multiplier)
        if num_combos > max_combos:
            num_combos = max_combos
        if num_combos == 0:
            return False
        self.multiplier = num_combos
        return True


class EveryNSecondsMainCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["TODO"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        return self._check_timed()


class InFeverCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_fever"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        return self.state.fever_active


class InPierceCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["TODO"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        return self.state.pierce_active


class OnAttackBuffActivateCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_condition"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in char_idxs:
            if self.state.ability_condition_active[idx][self.ability_idx]:
                return True
        return False


class OnCountDirectHitsCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_direct_attack"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.multiplier = 0
        amt = self._calc_abil_lv()
        for idx in self._only_mains(char_idxs):
            if self.state.direct_hits[idx] >= amt:
                self.multiplier += math.floor(self.state.direct_hits[idx] / amt)
        if self.multiplier == 0:
            return False
        return True


class SelfIsElementCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["TODO"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        element = element_ab_to_enum(self.ability.condition_target_element)
        for idx in self._only_mains(char_idxs):
            if self.state.party[idx].element != element:
                return False
        return True


class HPAbovePercentCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_hp_high"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in char_idxs:
            current_hp = self.state.party.current_hp[mains_only_index(idx)]
            max_hp = self.state.party.max_hp[mains_only_index(idx)]
            if (current_hp / max_hp) < self._calc_abil_lv():
                return False
        return True


class MultiballCountCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_multiball"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        return self.state.num_multiballs > self._calc_abil_lv()


class BuffActiveCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_condition"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in char_idxs:
            if len(self.state.buffs[main_index(idx)]) == 0:
                return False
        return True


class AttackBuffActiveCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_condition"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in self._only_mains(char_idxs):
            try:
                self.state.buffs[idx].index(StatusEffectKind.ATTACK)
            except ValueError:
                return False
        return True


class AttackBuffsOnSelfCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_condition_high_count"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.multiplier = 0
        for idx in self._only_mains(char_idxs):
            self.multiplier += (
                self.state.buffs[idx].count(StatusEffectKind.ATTACK)
                * self._calc_abil_lv()
            )
        if self.multiplier == 0:
            return False
        return True


class SkillGaugeAboveCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_skill_gauge_high"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        amt = self._calc_abil_lv()
        for idx in char_idxs:
            if self.state.skill_charge[main_index(idx)] <= amt:
                return False
        return True


class DebuffsOnEnemyCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return [
            "ability_description_during_trigger_kind_one_of_enemy_condition_high_count"
        ]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        enemy = self.state.enemy
        if enemy is None:
            return False
        self.multiplier = len(enemy.debuffs) * self._calc_abil_lv()
        return True


class PierceActiveCondition(WorldFlipperBaseCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_condition"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        return self.state.pierce_active
