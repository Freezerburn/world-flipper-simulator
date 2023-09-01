from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple

from .wfenum import CharPosition

if TYPE_CHECKING:
    from .wfchar import WorldFlipperCharacter
    from .wfability import WorldFlipperAbility
    from .wfenemy import Enemy


class GameState:
    def __init__(self):
        # 0: LEADER        (col 0)
        # 1: LEADER UNISON (col 1)
        # 2: MAIN          (col 1)
        # 3: UNISON        (col 1)
        # 4: MAIN          (col 2)
        # 5: UNISON        (col 2)
        self.party: list[Optional[WorldFlipperCharacter]] = [None] * 6
        self.levels = [1] * 6
        self.uncaps = [0] * 6
        # Each entry corresponds to the member at the same entry in party. Each
        # inner list int corresponds to the same number (+1) ability for that
        # character.
        self.ability_lvs = [[0] * 6] * 6
        self.skill_lvs = [0] * 6
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
        self.num_multiballs = 0
        self.buffs = [[], [], []]
        self.combos_reached: dict[int, int] = {}
        self.in_fever = False
        self.enemy: Optional[Enemy] = None

    def position(self, char: WorldFlipperCharacter) -> Optional[CharPosition]:
        try:
            idx = self.party.index(char)
            if idx == 0:
                return CharPosition.LEADER
            if idx % 2 == 0:
                return CharPosition.MAIN
            return CharPosition.UNISON
        except ValueError:
            return None

    def main_index(self, char_idx: int):
        if char_idx % 2 == 0:
            return char_idx
        return char_idx - 1

    def leader(self) -> Optional[WorldFlipperCharacter]:
        return self.party[0]

    def evolved(self, char: WorldFlipperCharacter) -> bool:
        try:
            idx = self.party.index(char)
            # A unit evoles when the entire MB1 has been unlocked. Effectively this means that the first
            # three abilities are level 6 (they are unlocked at LV1 and enhance 2-6) and the skill is
            # level 5 (skill is always unlocked, so it just needs to be enhanced 5 times).
            return self.ability_lvs[idx][:3] == [6] * 3 and self.skill_lvs[idx] == 5
        except ValueError:
            return False

    def set_member(
        self,
        char: Optional[WorldFlipperCharacter],
        position: CharPosition,
        column: int = -1,
        level=1,
        uncaps=0,
    ):
        if position == CharPosition.LEADER:
            column = 0
            position = CharPosition.MAIN

        offset = 0
        if position == CharPosition.UNISON:
            offset = 1
        idx = column * 2 + offset
        self.party[idx] = char
        self.levels[idx] = level
        self.uncaps[idx] = uncaps
        self.ability_lvs[idx] = [0] * 6
        self.ability_condition_active[idx] = [False] * 6

    def set_powerflips(self, lv: int, count: int):
        self.powerflips_by_lv[lv - 1] = count
        self.total_powerflips = sum(self.powerflips_by_lv)

    def set_skill_activations(self, char: int | WorldFlipperCharacter, count: int):
        if isinstance(char, int):
            self.skill_activations[char] = count
        else:
            self.skill_activations[self.party.index(char)] = count
        self.total_skill_activations = sum(self.skill_activations)

    def ability_index(self, ability: WorldFlipperAbility) -> Tuple[int, int]:
        for char_idx, char in enumerate(self.party):
            if char is None:
                continue
            for char_abs_idx, char_abs in enumerate(char.abilities):
                for char_ab in char_abs:
                    if char_ab == ability:
                        return char_idx, char_abs_idx
        return -1, -1
