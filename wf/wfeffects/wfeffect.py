from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from dataclasses import dataclass

from wf.wfdmgformula import DamageFormulaContext

if TYPE_CHECKING:
    from wf import WorldFlipperAbility, WorldFlipperCharacter, DamageFormulaContext
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
