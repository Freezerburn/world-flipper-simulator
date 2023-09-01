from __future__ import annotations

from typing import TYPE_CHECKING, Type
from abc import ABC
import math

from wf.wfenum import CharPosition
from wf.wfeffects.wfeffect import WorldFlipperCondition

if TYPE_CHECKING:
    from wf.wfchar import WorldFlipperCharacter
    from wf.wfeffects.wfeffect import WorldFlipperEffect


class WorldFlipperMainCondition(WorldFlipperCondition, ABC):
    def _calc_abil_lv(self) -> int:
        v_min = int(self.ability.main_condition_min) / 100_000
        v_max = int(self.ability.main_condition_max) / 100_000
        step = abs(v_max - v_min) / 5
        return v_min + step * (self.lv - 1)


class OnBattleStartMainCondition(WorldFlipperMainCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_first_flip"]

    def eval(self) -> bool:
        return self.should_run()


def NTimesCondition(following_ui_name: str) -> Type[WorldFlipperMainCondition]:
    class _NTimesCondition(WorldFlipperMainCondition):
        @staticmethod
        def ui_key() -> list[str]:
            return ["ability_description_n_times"]

        def eval(self) -> bool:
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


class OnSkillInvokeMainCondition(WorldFlipperMainCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_skill_invoke"]

    def eval(self) -> bool:
        activations_per_effect = self._calc_abil_lv()
        element = self.ability.element_enum(self.ability.main_condition_element)
        self.multiplier = 0
        for idx, p in enumerate(self.state.party):
            if p is None:
                continue
            # This buff can apply to individual units when they activate their own skill.
            # So if the target type indicates that scenario, we skip any skill activations
            # that are not for the target unit given to this function when calculating the
            # total multiplier.
            if self.ability.main_effect_target == "7" and idx != self.target_char_idx:
                continue
            if element is None or p.element == element:
                self.multiplier += (
                    self.state.skill_activations[idx] / activations_per_effect
                )
        # If we didn't achieve the activation condition across the entire party, then this damage
        # calculation is invalid. The best example of this is if there's an activation condition
        # that has a character getting a buff when activating a skill, but it has an element
        # restriction on it. In that case if the unit isn't that element, then we'd end up with
        # an invalid formula.
        if self.multiplier == 0:
            return False
        # There are effect types that don't care about multipliers. An example of this is
        # AHanabi's ability 2, which deals damage to all units when a skill is activated with
        # a cooldown on how often this can occur.
        if self.ability.main_effect_max_multiplier == "(None)":
            max_mult = 1
        else:
            max_mult = int(self.ability.main_effect_max_multiplier)
        if self.multiplier > max_mult:
            self.multiplier = max_mult
        return True


class OnSkillGaugeReach100MainCondition(WorldFlipperMainCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_skill_max"]

    def eval(self) -> bool:
        self.multiplier = self._calc_multiplier(
            int(self.ability.main_effect_max_multiplier),
            self.state.times_skill_reached_100[self.ability_char_idx],
        )
        return True


class PartyMembersAddedMainCondition(WorldFlipperMainCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_member"]

    def eval(self) -> bool:
        num_element = 0
        element = self.ability.element_enum(self.ability.condition_target_element)
        for p in self.state.party:
            if p is None:
                continue
            if p.element == element:
                num_element += 1
        self.multiplier = self._calc_multiplier(
            int(self.ability.main_effect_max_multiplier),
            num_element,
        )
        return True


class Lv3PowerFlipsMainCondition(WorldFlipperMainCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_power_flip_lv"]

    def eval(self) -> bool:
        self.multiplier = self._calc_multiplier(
            int(self.ability.main_effect_max_multiplier),
            self.state.powerflips_by_lv[2],
        )
        return True


class ComboReachedMainCondition(WorldFlipperMainCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_combo"]

    def eval(self) -> bool:
        combo_req = self._calc_abil_lv()
        num_combos = self.state.combos_reached.get(combo_req, 0)
        max_combos = int(self.ability.main_effect_max_multiplier)
        if num_combos > max_combos:
            num_combos = max_combos
        if num_combos == 0:
            return False
        self.multiplier = num_combos
        return True
