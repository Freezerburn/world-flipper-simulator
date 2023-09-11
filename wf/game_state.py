from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple

from .character import WorldFlipperCharacter
from .party import Party

if TYPE_CHECKING:
    from .ability import WorldFlipperAbility
    from .enemy import Enemy


class GameState:
    def __init__(self):
        self.seconds_passed = -1
        self.party = Party()
        # Same layout as ability_lvs.
        self.ability_condition_active = [[False] * 6] * 6
        # Each entry corresponds to the member at the same index in party.
        self.skill_hits = [0] * 6
        self.total_skill_hits = 0
        # Same layout as party.
        self.skill_activations = [0] * 6
        self.total_skill_activations = 0
        self.times_skill_reached_100 = [0] * 3
        self.skill_gauge_max = [100] * 3
        self.skill_charge = [0] * 3
        self.powerflips_by_lv = [0] * 3
        self.total_powerflips = 0
        self.total_powerflip_hits = 0
        self.total_ball_flips = 0
        self.direct_hits = [0] * 3
        self.total_direct_hits = 0
        self.num_multiballs = 0
        self.buffs = [[], [], []]
        self.combos_reached: dict[int, int] = {}
        self.fever_active = False
        self.pierce_active = False
        self.enemy: Optional[Enemy] = None

    def set_powerflips(self, lv: int, count: int):
        self.powerflips_by_lv[lv - 1] = count
        self.total_powerflips = sum(self.powerflips_by_lv)

    def set_skill_activations(self, char: int | WorldFlipperCharacter, count: int):
        if isinstance(char, int):
            self.skill_activations[char] = count
        else:
            self.skill_activations[self._party.index(char)] = count
        self.total_skill_activations = sum(self.skill_activations)
