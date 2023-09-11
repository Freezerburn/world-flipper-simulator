from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple, Self

from .enum import CharPosition
from .character import WorldFlipperCharacter

if TYPE_CHECKING:
    from .ability import WorldFlipperAbility


def _index(position: CharPosition, column: int):
    match position:
        case CharPosition.LEADER:
            return 0
        case CharPosition.MAIN:
            return column * 2
        case CharPosition.UNISON:
            return column * 2 + 1
        case _:
            raise ValueError(f"Unknown position type: {position}")


def unison_index(char_idx: int):
    if char_idx % 2 == 1:
        return char_idx
    return char_idx + 1


def mains_only_index(char_idx: int) -> int:
    if char_idx % 2 == 0:
        return int(char_idx / 2)
    return int((char_idx - 1) / 2)


def main_index(char_idx: int):
    if char_idx % 2 == 0:
        return char_idx
    return char_idx - 1


class Party:
    def __init__(self):
        # 0: LEADER        (col 0)
        # 1: LEADER UNISON (col 1)
        # 2: MAIN          (col 1)
        # 3: UNISON        (col 1)
        # 4: MAIN          (col 2)
        # 5: UNISON        (col 2)
        self._party: list[Optional[WorldFlipperCharacter]] = [None] * 6
        self.levels = [1] * 6
        self.uncaps = [0] * 6
        self.max_hp = [0.0] * 3
        self.current_hp = [0.0] * 3
        # Each entry corresponds to the member at the same entry in party. Each
        # inner list int corresponds to the same number (+1) ability for that
        # character.
        self.ability_lvs = [[0] * 6] * 6
        self.skill_lvs = [0] * 6

    def position(
        self, char: Optional[WorldFlipperCharacter | int]
    ) -> Optional[CharPosition]:
        if char is None:
            return None

        if isinstance(char, WorldFlipperCharacter):
            try:
                idx = self._party.index(char)
            except ValueError:
                return None
        else:
            idx = char
        if idx == 0:
            return CharPosition.LEADER
        if idx % 2 == 0:
            return CharPosition.MAIN
        return CharPosition.UNISON

    def leader(self) -> Optional[WorldFlipperCharacter]:
        return self._party[0]

    def is_evolved(self, char: WorldFlipperCharacter) -> bool:
        try:
            idx = self._party.index(char)
            # A unit evoles when the entire MB1 has been unlocked. Effectively this means that the first
            # three abilities are level 6 (they are unlocked at LV1 and enhance 2-6) and the skill is
            # level 5 (skill is always unlocked, so it just needs to be enhanced 5 times).
            return (
                self.ability_lvs[idx][0] >= 1
                and self.ability_lvs[idx][1] >= 1
                and self.ability_lvs[idx][2] >= 1
                and self.skill_lvs[idx] >= 1
            )
        except ValueError:
            return False

    def char_atk(self, char: WorldFlipperCharacter | int) -> float:
        if isinstance(char, int):
            level = self.levels[char]
            uncaps = self.uncaps[char]
            char = self._party[char]
        else:
            idx = self._party.index(char)
            level = self.levels[idx]
            uncaps = self.uncaps[idx]
        return char.attack(self.is_evolved(char), level, uncaps)

    def char_hp(self, char: WorldFlipperCharacter | int) -> float:
        if isinstance(char, int):
            level = self.levels[char]
            uncaps = self.uncaps[char]
            char = self._party[char]
        else:
            idx = self._party.index(char)
            level = self.levels[idx]
            uncaps = self.uncaps[idx]
        if char is None:
            return 0
        return char.hp(self.is_evolved(char), level, uncaps)

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

        if char is not None:
            try:
                existing = self._party.index(char)
                to_idx = _index(position, column)
                if to_idx == existing:
                    return
                self.swap(existing, to_idx)
            except ValueError:
                self._set_char(char, position, column, level, uncaps)
        else:
            self._set_char(None, position, column, level, uncaps)

    def _set_char(
        self,
        char: Optional[WorldFlipperCharacter],
        position: CharPosition,
        column: int = -1,
        level=1,
        uncaps=0,
    ):
        idx = _index(position, column)
        self._party[idx] = char
        self.levels[idx] = level
        self.uncaps[idx] = uncaps
        self.ability_lvs[idx] = [0] * 6
        self._update_hp()

    def _update_hp(self):
        for column in range(3):
            idx = column * 2
            char = self._party[idx]

            if char is not None:
                self.max_hp[column] = self.char_hp(char)
                if self._party[idx + 1] is not None:
                    self.max_hp[column] += self.char_hp(idx + 1) / 4
            else:
                if self._party[idx + 1] is not None:
                    self.max_hp[column] = self.char_hp(idx + 1) / 4
                else:
                    self.max_hp[column] = 0
            self.current_hp[column] = self.max_hp[column]

    def swap(self, char_idx: int, to_idx: int):
        self._party[to_idx], self._party[char_idx] = (
            self._party[char_idx],
            self._party[to_idx],
        )
        self.levels[to_idx], self.levels[char_idx] = (
            self.levels[char_idx],
            self.levels[to_idx],
        )
        self.uncaps[to_idx], self.uncaps[char_idx] = (
            self.uncaps[char_idx],
            self.uncaps[to_idx],
        )
        self.ability_lvs[to_idx], self.ability_lvs[char_idx] = (
            self.ability_lvs[char_idx],
            self.ability_lvs[to_idx],
        )
        self._update_hp()

    def ability_index(self, ability: WorldFlipperAbility) -> Tuple[int, int]:
        for char_idx, char in enumerate(self._party):
            if char is None:
                continue
            for char_abs_idx, char_abs in enumerate(char.abilities):
                for char_ab in char_abs:
                    if char_ab == ability:
                        return char_idx, char_abs_idx
        return -1, -1

    def index(self, key: Optional[WorldFlipperCharacter]) -> int:
        return self._party.index(key)

    def __iter__(self):
        for p in self._party:
            yield p

    def __getitem__(self, idx: int | WorldFlipperCharacter):
        if isinstance(idx, int):
            return self._party[idx]
        elif isinstance(idx, WorldFlipperCharacter):
            pass
        raise IndexError(f"Unknown index type: {type(idx).__name__}")

    def __setitem__(self, idx: int, value: Optional[WorldFlipperCharacter]):
        position = self.position(idx)
        column = mains_only_index(idx)
        self.set_member(self._party[idx], position, column)

    def __delitem__(self, idx: int):
        self.__setitem__(idx, None)
