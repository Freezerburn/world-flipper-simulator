from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from dataclasses import dataclass
import math

from wf.wfenum import CharPosition

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
    target_char: WorldFlipperCharacter
    ability_char: WorldFlipperCharacter
    ctx: DamageFormulaContext

    multiplier: int = 1


class WorldFlipperEffect(ABC):
    @staticmethod
    @abstractmethod
    def ui_key() -> list[str]:
        pass

    def __init__(self, params: EffectParams):
        self.ui_name = params.ui_name
        self.ability = params.ability
        self.state = params.state
        self.target_char = params.target_char
        self.ability_char = params.ability_char

        self.ctx = params.ctx
        self.multiplier = params.multiplier

        self.target_char_idx = self.state.party.index(self.target_char)
        self.target_char_position = self.state.position(self.target_char)
        self.ability_char_idx, self.ability_idx = self.state.ability_index(self.ability)
        self.ability_char_position = self.state.position(self.ability_char)
        self.lv = self.state.ability_lvs[self.ability_char_idx][self.ability_idx]

    @abstractmethod
    def eval(self) -> bool:
        pass

    @abstractmethod
    def _calc_abil_lv(self) -> int:
        pass


class WorldFlipperCondition(WorldFlipperEffect, ABC):
    def _calc_multiplier(self, cap: int, count: int) -> int:
        abil = self._calc_abil_lv()
        times = math.floor(count / abil)
        if times >= cap:
            times = cap
        return times

    def should_run(self) -> bool:
        if self.target_char_position is None:
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
            self.target_char,
        ):
            return False
        return True

    def _target_applies_to(
        self, target: str, element: str, char: WorldFlipperCharacter
    ) -> bool:
        match target:
            case "":
                return True
            case "0":
                return self.ability_char.internal_name == char.internal_name
            case "1":
                return self.ability_char.internal_name != char.internal_name
            case "2":
                return char.position == CharPosition.LEADER
            case "5" | "7":
                if not element:
                    return True
                else:
                    return char.element == self.ability.element_enum(element)
            case "8":
                # TODO: Implement multiball
                return False

        return False
