from typing import TYPE_CHECKING, Optional

from .wfenum import CharPosition

if TYPE_CHECKING:
    from .wfchar import WorldFlipperCharacter


class GameState:
    def __init__(self):
        # 0: LEADER        (col 0)
        # 1: LEADER UNISON (col 1)
        # 2: MAIN          (col 1)
        # 3: UNISON        (col 1)
        # 4: MAIN          (col 2)
        # 5: UNISON        (col 2)
        self.party: list[Optional["WorldFlipperCharacter"]] = [None] * 6
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

    def set_member(
        self,
        char: Optional["WorldFlipperCharacter"],
        column: int,
        position: CharPosition,
    ):
        if position == CharPosition.LEADER:
            self.party[0] = char
            return

        offset = 0
        if position == CharPosition.UNISON:
            offset = 1
        self.party[column * 2 + offset] = char

    def set_powerflips(self, lv: int, count: int):
        self.powerflips_by_lv[lv] = count
        self.total_powerflips = sum(self.powerflips_by_lv)
