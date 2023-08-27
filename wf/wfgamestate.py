from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from .wfenum import CharPosition

if TYPE_CHECKING:
    from .wfchar import WorldFlipperCharacter
    from .wfability import WorldFlipperAbility


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
        # Same layout as ability_lvs.
        self.ability_condition_active = [[False] * 6] * 6
        # Each entry corresponds to the member at the same index in party.
        self.skill_hits = [0] * 6
        self.total_skill_hits = 0
        self.powerflips_by_lv = [0] * 3
        self.total_powerflips = 0
        self.total_powerflip_hits = 0
        self.enemy = None

    def position(self, char: WorldFlipperCharacter) -> Optional[CharPosition]:
        for idx, p in enumerate(self.party):
            if p is None:
                continue
            if p.internal_name == char.internal_name:
                if idx == 0:
                    return CharPosition.LEADER
                if idx % 2 == 0:
                    return CharPosition.MAIN
                return CharPosition.UNISON
        return None

    def leader(self) -> Optional[CharPosition]:
        return self.party[0]

    def evolved(self, char: WorldFlipperCharacter) -> bool:
        # TODO: Implement
        # Basically checking if all MB1 abilities are unlocked and the unit has reached a specific level?
        # That might be the MB2 unlock requirement, evolve might be a bit different.
        return False

    def set_member(
        self,
        char: Optional[WorldFlipperCharacter],
        column: int,
        position: CharPosition,
    ):
        if position == CharPosition.LEADER:
            self.party[0] = char
            return

        offset = 0
        if position == CharPosition.UNISON:
            offset = 1
        idx = column * 2 + offset
        self.party[idx] = char
        self.ability_lvs[idx] = [0] * 6
        self.ability_condition_active[idx] = [False] * 6

    def set_powerflips(self, lv: int, count: int):
        self.powerflips_by_lv[lv] = count
        self.total_powerflips = sum(self.powerflips_by_lv)

    def char_index(self, char: WorldFlipperCharacter) -> int:
        for idx, p in enumerate(self.party):
            if p.internal_name == char.internal_name:
                return idx
        return -1

    def ability_index(self, ability: WorldFlipperAbility) -> (int, int):
        for char_idx, char in enumerate(self.party):
            for char_abs_idx, char_abs in enumerate(char.abilities):
                for char_ab in char_abs:
                    if char_ab.name == ability.name:
                        return char_idx, char_abs_idx
        return -1, -1
