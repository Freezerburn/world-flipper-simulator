from __future__ import annotations

from typing import TYPE_CHECKING, Type
from abc import ABC
import math

from wf.wfenum import CharPosition, element_ab_to_enum
from wf.wfeffects.wfeffect import WorldFlipperCondition

if TYPE_CHECKING:
    from wf.wfchar import WorldFlipperCharacter
    from wf.wfeffects.wfeffect import WorldFlipperBaseEffect


class OnBattleStartMainCondition(WorldFlipperCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_first_flip"]

    def eval(self) -> bool:
        return self.should_run()


def NTimesCondition(following_ui_name: str) -> Type[WorldFlipperCondition]:
    class _NTimesCondition(WorldFlipperCondition):
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


class OnSkillInvokeMainCondition(WorldFlipperCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_skill_invoke"]

    def eval(self) -> bool:
        activations_per_effect = self._calc_abil_lv()
        element = element_ab_to_enum(self.ability.main_condition_element)
        self.multiplier = 0
        match (self.ability.main_condition_target, self.ability.main_effect_target):
            case ("0", "0"):
                # When own skill activates, buff self.
                if element is not None and self.eval_char.element != element:
                    return False
                self.multiplier += (
                    self.state.skill_activations[self.eval_char_idx]
                    / activations_per_effect
                )
            case ("5", "7"):
                # When anyone's skill activates, buff them.
                if self.eval_char_idx != self.ability_char_idx:
                    return False
                if element is None or self.eval_char.element != element:
                    return False
                self.multiplier += (
                    self.state.skill_activations[self.eval_char_idx]
                    / activations_per_effect
                )
            case ("7", "0") | ("7", ""):
                # When someone's skill activates, buff self/all.
                for idx, p in enumerate(self.state.party):
                    if p is None:
                        continue
                    if element is None or p.element == element:
                        self.multiplier += (
                            self.state.skill_activations[idx] / activations_per_effect
                        )
            case _:
                raise RuntimeError(
                    f"[{self.ability.name} Unknown target combo: "
                    f"{self.ability.main_condition_target}, "
                    f"{self.ability.main_effect_target}"
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
            max_mult = 9999
        else:
            max_mult = int(self.ability.main_effect_max_multiplier)
        if self.multiplier > max_mult:
            self.multiplier = max_mult
        return True


class OnSkillGaugeReach100MainCondition(WorldFlipperCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_skill_max"]

    def eval(self) -> bool:
        self.multiplier = self._calc_multiplier(
            int(self.ability.main_effect_max_multiplier),
            self.state.times_skill_reached_100[self.ability_char_idx],
        )
        return True


class PartyMembersAddedMainCondition(WorldFlipperCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_member"]

    def eval(self) -> bool:
        num_element = 0
        element = element_ab_to_enum(self.ability.condition_target_element)
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


class Lv3PowerFlipsMainCondition(WorldFlipperCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_power_flip_lv"]

    def eval(self) -> bool:
        self.multiplier = self._calc_multiplier(
            int(self.ability.main_effect_max_multiplier),
            self.state.powerflips_by_lv[2],
        )
        return True


class ComboReachedMainCondition(WorldFlipperCondition):
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


class InFeverCondition(WorldFlipperCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_instant_trigger_kind_fever"]

    def eval(self) -> bool:
        return self.state.in_fever
