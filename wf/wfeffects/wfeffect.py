from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from dataclasses import dataclass
import math

from wf.wfenum import CharPosition, element_ab_to_enum, AbilityElementType, Element

if TYPE_CHECKING:
    from wf import (
        WorldFlipperAbility,
        WorldFlipperCharacter,
        DamageFormulaContext,
    )
    from wf.wfgamestate import GameState


@dataclass
class EffectParams:
    ui_name: list[str]
    ability: WorldFlipperAbility
    state: GameState
    eval_char: WorldFlipperCharacter
    ability_char: WorldFlipperCharacter
    ctx: DamageFormulaContext

    multiplier: int = 1


class WorldFlipperBaseEffect(ABC):
    @staticmethod
    @abstractmethod
    def ui_key() -> list[str]:
        pass

    def __init__(self, params: EffectParams):
        self.ui_name = params.ui_name
        self.ability = params.ability
        self.state = params.state
        self.eval_char = params.eval_char
        self.ability_char = params.ability_char

        self.ctx = params.ctx
        self.multiplier = params.multiplier

        self.eval_char_idx = self.state.party.index(self.eval_char)
        self.eval_main_idx = self.state.main_index(self.eval_char_idx)
        self.eval_char_position = self.state.position(self.eval_char)
        self.ability_char_idx, self.ability_idx = self.state.ability_index(self.ability)
        self.ability_main_idx = self.state.main_index(self.ability_char_idx)
        self.ability_char_position = self.state.position(self.ability_char)
        self.lv = self.state.ability_lvs[self.ability_char_idx][self.ability_idx]

    def eval(self) -> bool:
        if self.ability.is_main_effect():
            if self.is_condition():
                target = self.ability.main_condition_target
                # SPECIAL CASE: I *think* when an ability has "if self is a(n) <element> character", this
                # gets set to 2 and then the random other element index gets set to an element. I first
                # noticed this for Selene's AB5. The normal locations you would expect to have an element
                # for a condition don't have elements set in them in this case.
                if self.ability.party_condition_index == "2":
                    element = element_ab_to_enum(self.ability.party_condition_element)
                elif target == "":
                    element = element_ab_to_enum(self.ability.condition_target_element)
                else:
                    element = element_ab_to_enum(self.ability.main_condition_element)
            else:
                element = element_ab_to_enum(self.ability.main_effect_element)
                target = self.ability.main_effect_target
        else:
            if self.is_condition():
                element = element_ab_to_enum(self.ability.continuous_condition_element)
                target = self.ability.continuous_condition_target
            else:
                element = element_ab_to_enum(self.ability.continuous_effect_element)
                target = self.ability.continuous_effect_target

        match target:
            case "0":
                # Own/self.
                # NOTE: As far as I'm aware, this target always refers to the unit whose ability is
                # being evaluated. NOT the unit that was passed as an argument for evaluation.
                main = self.state.party[self.ability_main_idx]
                if main is None:
                    return False
                if element is not None and main.element != element:
                    return False
                return self._apply_effect([self.ability_char_idx])

            case "2":
                # Leader.
                leader = self.state.party[0]
                if leader is None:
                    return False
                if element is not None and leader.element != element:
                    return False
                return self._apply_effect([0])

            case "" | "1" | "5":
                # All (other) party members.
                # "1" means "all other". In this case I'm defining "other" as any unit that is not the
                # unit the ability came from.

                # SPECIAL CASE: Condition target 5 with effect target 7. This means that whenever an
                # individual unit does a thing, it affects only itself.
                if target == "5":
                    if (
                        self.ability.is_main_effect()
                        and self.ability.main_effect_target == "7"
                    ) or (
                        self.ability.is_continuous_effect()
                        and self.ability.continuous_effect_target == "7"
                    ):
                        main = self.state.party[self.eval_main_idx]
                        if main is None:
                            return False
                        if element is not None and main.element != element:
                            return False
                        return self._apply_effect([self.eval_main_idx])

                char_idxs: list[int] = []
                for idx, p in enumerate(self.state.party):
                    if p is None:
                        continue
                    if target == "1" and idx == self.ability_char_idx:
                        continue
                    main = self.state.party[self.state.main_index(idx)]
                    if main is None:
                        continue
                    if element is None or main.element == element:
                        char_idxs.append(idx)
                if len(char_idxs) == 0:
                    return False
                return self._apply_effect(char_idxs)

            case "7":
                # Triggering unit.

                # SPECIAL CASE: When the condition target is a triggering unit, and the effect target is
                # a self unit (or a global effect), then we should check the entire party.
                if (
                    self.ability.is_main_effect()
                    and self.ability.main_effect_target in ("0", "")
                ) or (
                    self.ability.is_continuous_effect()
                    and self.ability.continuous_effect_target in ("0", "")
                ):
                    char_idxs: list[int] = []
                    for idx, p in enumerate(self.state.party):
                        if p is None:
                            continue
                        main = self.state.party[self.state.main_index(idx)]
                        if main is None:
                            continue
                        if element is None or main.element == element:
                            char_idxs.append(idx)
                    if len(char_idxs) == 0:
                        return False
                    return self._apply_effect(char_idxs)

                main = self.state.party[self.eval_main_idx]
                if main is None:
                    return False
                if element is not None and main.element != element:
                    return False
                return self._apply_effect([self.eval_char_idx])

            case _:
                raise RuntimeError(f"[{self.ability.name}] Unhandled target: {target}")

    def _only_mains(self, char_idxs: list[int]):
        main_idxs: set[int] = set()
        for idx in char_idxs:
            main_idxs.add(self.state.main_index(idx))
        return main_idxs

    @abstractmethod
    def _apply_effect(self, char_idxs: list[int]) -> bool:
        pass

    @abstractmethod
    def effect_min(self) -> int:
        pass

    @abstractmethod
    def effect_max(self) -> int:
        pass

    @abstractmethod
    def is_condition(self) -> bool:
        pass

    def _calc_abil_lv(self) -> int:
        """
        Abilities generally have a linear increment on each level they gain on the mana board between a minimum
        and a maximum. This calculates the current value for an ability based on its current level.
        """
        v_min = self.effect_min() / 100_000
        v_max = self.effect_max() / 100_000
        step = abs(v_max - v_min) / 5
        amt = v_min + step * (self.lv - 1)
        if not self.is_condition():
            amt *= self.multiplier
        return amt

    def is_target_main(self) -> bool:
        if self.eval_char_position == CharPosition.LEADER:
            return True
        if self.eval_char_position == CharPosition.MAIN:
            return True
        return False


class WorldFlipperEffect(WorldFlipperBaseEffect, ABC):
    def is_condition(self) -> bool:
        return False

    def effect_min(self) -> int:
        if self.ability.is_main_effect():
            return int(self.ability.main_effect_min)
        else:
            return int(self.ability.continuous_effect_min)

    def effect_max(self) -> int:
        if self.ability.is_main_effect():
            return int(self.ability.main_effect_max)
        else:
            return int(self.ability.continuous_effect_max)


class WorldFlipperCondition(WorldFlipperBaseEffect, ABC):
    def is_condition(self) -> bool:
        return True

    def effect_min(self) -> int:
        if self.ability.is_main_effect():
            return int(self.ability.main_condition_min)
        else:
            return int(self.ability.continuous_condition_min)

    def effect_max(self) -> int:
        if self.ability.is_main_effect():
            return int(self.ability.main_condition_max)
        else:
            return int(self.ability.continuous_condition_max)

    def _calc_multiplier(self, cap: int, count: int) -> int:
        abil = self._calc_abil_lv()
        times = math.floor(count / abil)
        if times >= cap:
            times = cap
        return times

    def should_run(self) -> bool:
        if self.eval_char_position is None:
            return False
        if self.ability_char_idx == -1:
            return False
        if self.lv == 0:
            return False
        # Don't apply an effect if it requires a character to be in a main slot and the unit is
        # a unison.
        if (
            self.ability.requires_main
            and self.ability_char_position == CharPosition.UNISON
        ):
            return False

        if self.ability.is_main_effect():
            target = self.ability.main_effect_target
            element = self.ability.main_effect_element
        else:
            target = self.ability.continuous_effect_target
            element = self.ability.continuous_effect_element
        if not self._target_applies_to(
            target,
            element,
            self.eval_char,
        ):
            return False
        return True

    def _target_applies_to(
        self, target: str, element: AbilityElementType, char: WorldFlipperCharacter
    ) -> bool:
        # Abilities only ever apply to the main units in the party. Code should generally only ever be
        # trying to apply them to main units, but we want to make sure to guard against it here and
        # let tests that deliberately do the wrong thing pass so that we know the code is solid.
        if not self.is_target_main():
            return False

        match target:
            case "":
                return True
            case "0":
                # If the target char is the same as the ability char, apply the ability.
                if self.ability_char.internal_name == char.internal_name:
                    return True
                # Otherwise since index 0 is "self/own", we want to check if the ability belongs to the
                # unison for a main unit, and if that's the case then we want to apply it.
                unison = self.state.party[self.state.unison_index(self.eval_char_idx)]
                if unison is None:
                    return False
                return unison.internal_name == self.ability_char.internal_name
            case "1":
                return self.ability_char.internal_name != char.internal_name
            case "2":
                return char.position == CharPosition.LEADER
            case "5" | "7":
                if not element or element == "(None)":
                    return True
                else:
                    return char.element == element_ab_to_enum(element)
            case "8":
                # TODO: Implement multiball
                return False

        return False
