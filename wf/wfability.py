from __future__ import annotations
from typing import Literal, Optional, TYPE_CHECKING, cast

from .wfdmgformula import DamageFormulaContext
from .wfenum import AbilityElementType
from .wfgamestate import GameState

from .wfeffects.wfeffect import EffectParams
from .wfeffects.wfmaineffectmapping import main_condition_mapping, main_effect_mapping
from .wfeffects.wfcontinuousmapping import (
    continuous_condition_mapping,
    continuous_effect_mapping,
)

if TYPE_CHECKING:
    from .wfchar import WorldFlipperCharacter

EffectType = Literal["0", "1"]

_PERCENT_CONVERT = 100_000
_COUNT_CONVERT = 100_000
_SEC_CONVERT = 600_000

# TODO: Going to need something that can evaluate an ability to figure out what UI elements to show.
# Not all abilities are going to need a toggle to say whether or not they're going to be active, as
# an example. Things that might need this would be stuff like a continuous effect that has a
# condition for when the effect is going to be applied. Or showing a slider or something for when
# something requires a certain number of powerflips so that the user can decide what level of buff
# is currently active for the purposes of calculations.


class EffectParameters:
    def __init__(self, idx: str, target: str, element: str, min_v: str, max_v: str):
        self.idx = idx
        self.target = target
        self.element = element
        self.min_v = min_v
        self.max_v = max_v


class WorldFlipperAbility:
    def __init__(self, data: list[str], from_char):
        self.from_char = from_char
        self.name = data[0]
        self.requires_main = data[1] == "false"
        self.ability_statue_group = data[2]
        self.effect_type: EffectType = cast(
            EffectType, data[3]
        )  # 0 for "main effect", 1 for continuous
        self.party_condition_index = data[4]  # TODO: Verify
        self.slot5 = data[5]
        self.slot6 = data[6]
        self.slot7 = data[7]
        self.slot8 = data[8]
        self.party_condition_element = cast(AbilityElementType, data[9])  # TODO: Verify
        self.slot10 = data[10]
        self.slot11 = data[11]
        self.slot12 = data[12]
        self.slot13 = data[13]
        self.slot14 = data[14]
        self.slot15 = data[15]
        self.slot16 = data[16]
        self.slot17 = data[17]
        self.slot18 = data[18]
        self.slot19 = data[19]
        self.slot20 = data[20]
        self.slot21 = data[21]
        self.slot22 = data[22]
        self.slot23 = data[23]
        self.slot24 = data[24]
        self.main_condition_index = data[25]
        self.main_condition_target = data[26]
        self.main_condition_element = cast(AbilityElementType, data[27])
        self.main_condition_min = data[28]
        self.main_condition_max = data[29]
        # Valid values:
        # ""
        # "<number>"
        # "(None)"
        self.main_effect_max_multiplier = data[30]
        self.cooldown_time = data[31]  # Seconds multiplied by 60.
        self.condition_target_element = cast(AbilityElementType, data[32])
        self.slot33 = data[33]
        self.slot34 = data[34]
        self.slot35 = data[35]
        self.slot36 = data[36]
        self.slot37 = data[37]
        self.slot38 = data[38]
        self.slot39 = data[39]
        self.slot40 = data[40]
        self.slot41 = data[41]
        self.main_effect_index = data[42]
        self.main_effect_target = data[43]
        # Element here is used when the effect target needs to discriminate on which characters
        # it's going to actually do something to. e.g.: Increase attack damage for all
        # Water units, versus all units.
        self.main_effect_element = cast(AbilityElementType, data[44])
        self.main_effect_min = data[45]
        self.main_effect_max = data[46]
        self.slot47 = data[47]
        self.slot48 = data[48]
        self.slot49 = data[49]
        self.slot50 = data[50]
        # Duration stored in seconds * 6,000,000
        # NOTE: In general it seems like this can be "added" to any main effect in order to
        # give it some kind of time limit. It doesn't seem to be specific to any particular
        # index.
        self.main_effect_duration_min = data[51]
        self.main_effect_duration_max = data[52]
        # If a main effect is one that has a duration applied to it, it might be able
        # to stack the effect. This provides the max stacks/multiplier for that effect.
        self.main_effect_incremental_max_multiplier = data[53]
        self.slot54 = data[54]
        self.slot55 = data[55]
        self.slot56 = data[56]
        self.slot57 = data[57]
        self.slot58 = data[58]
        self.slot59 = data[59]
        self.slot60 = data[60]
        self.continuous_condition_index = data[61]
        self.continuous_condition_target = data[62]
        self.continuous_condition_element = cast(AbilityElementType, data[63])
        self.continuous_condition_min = data[64]
        self.continuous_condition_max = data[65]
        self.continuous_effect_max_multiplier = data[66]  # TODO: Verify
        self.slot67 = data[67]
        # This gets set to "1" for 1st Anniversary Celtie's ability 1, don't know what it does though.
        self.slot68 = data[68]
        self.slot69 = data[69]
        self.slot70 = data[70]
        self.slot71 = data[71]
        self.slot72 = data[72]
        self.continuous_effect_index = data[73]
        self.continuous_effect_target = data[74]
        self.continuous_effect_element = cast(AbilityElementType, data[75])
        self.continuous_effect_min = data[76]
        self.continuous_effect_max = data[77]
        self.slot78 = data[78]
        self.slot79 = data[79]
        self.slot80 = data[80]
        self.slot81 = data[81]
        self.slot82 = data[82]

    def is_main_effect(self) -> bool:
        return self.effect_type == "0"

    def is_continuous_effect(self) -> bool:
        return self.effect_type == "1"

    def effect_type_name(self) -> str:
        if self.is_main_effect():
            return "main"
        else:
            return "continuous"

    def main_condition(self) -> EffectParameters:
        return EffectParameters(
            self.main_condition_index,
            self.main_condition_target,
            self.main_condition_element,
            self.main_condition_min,
            self.main_condition_max,
        )

    def main_effect(self) -> EffectParameters:
        return EffectParameters(
            self.main_effect_index,
            self.main_effect_target,
            self.main_effect_element,
            self.main_effect_min,
            self.main_effect_max,
        )

    def element_friendly(self, element):
        if element == "Red":
            return "Fire"
        elif element == "Yellow":
            return "Thunder"
        elif element == "Green":
            return "Wind"
        elif element == "Blue":
            return "Water"
        elif element == "White":
            return "Light"
        elif element == "Black":
            return "Dark"
        else:
            raise RuntimeError(f"[{self.name}] Unknown element: {element}")

    def target_index_friendly(self, target, element=None):
        """
        0: this unit
        1: all other allied units
        2: Leader
        5: All(?)/elemental unit
        7: Unit that triggered the condition
        8: Multiballs
        """
        if target == "0":
            return "this unit"
        elif target == "1":
            return "all other allied units"
        elif target == "2":
            return "Leader"
        elif target == "5":
            if element is None:
                return "all unit"
            else:
                return f"{self.element_friendly(element)} unit"
        elif target == "7":
            return "that unit"
        elif target == "8":
            return "Multiballs"
        else:
            raise RuntimeError(f"[{self.name}] Unknown target index: {target}")

    def condition_ui(self) -> list[str]:
        if self.condition_index() not in self._condition_mapping():
            raise RuntimeError(
                f"[{self.name} Unknown {self.effect_type_name()} condition index: "
                f"{self.condition_index()}"
            )
        return self._condition_mapping()[self.condition_index()].ui_key()

    def effect_ui(self) -> list[str]:
        if self.effect_index() not in self._effect_mapping():
            raise RuntimeError(
                f"[{self.name} Unknown {self.effect_type_name()} condition index: "
                f"{self.effect_index()}"
            )
        ret = []
        for e in self._effect_mapping()[self.effect_index()]:
            for key in e.ui_key():
                ret.append(key)
        return ret

    def condition_index(self):
        if self.is_main_effect():
            return self.main_condition_index
        else:
            return self.continuous_condition_index

    def effect_index(self):
        if self.is_main_effect():
            return self.main_effect_index
        else:
            return self.continuous_effect_index

    def _condition_mapping(self):
        if self.is_main_effect():
            return main_condition_mapping
        else:
            return continuous_condition_mapping

    def _effect_mapping(self):
        if self.is_main_effect():
            return main_effect_mapping
        else:
            return continuous_effect_mapping

    def _eval_effect(
        self,
        char: WorldFlipperCharacter,
        state: GameState,
    ) -> Optional[DamageFormulaContext]:
        condition_ui = self.condition_ui()
        effect_ui = self.effect_ui()

        if self.condition_index() not in self._condition_mapping():
            raise RuntimeError(
                f"[{self.name}] Unknown {self.effect_type_name()} condition: "
                f"{self.condition_index()}"
            )
        if self.effect_index() not in self._effect_mapping():
            raise RuntimeError(
                f"[{self.name}] Unknown {self.effect_type_name()} effect: "
                f"{self.effect_index()}"
            )

        ab_char_idx, _ = state.ability_index(self)
        ab_char = state.party[ab_char_idx]
        if ab_char is None:
            raise RuntimeError(
                f"Impossible state: Found ability char but was None in party."
            )
        ctx = DamageFormulaContext()
        condition_param = EffectParams(condition_ui, self, state, char, ab_char, ctx)
        effect_param = EffectParams(effect_ui, self, state, char, ab_char, ctx)

        condition = self._condition_mapping()[self.condition_index()](condition_param)

        if not condition.should_run():
            return None
        if not condition.eval():
            return None
        effect_param.multiplier = condition.multiplier
        for e in self._effect_mapping()[self.effect_index()]:
            if not e(effect_param).eval():
                return None
        return effect_param.ctx

    def eval_effect(
        self,
        char: WorldFlipperCharacter,
        state: GameState,
    ) -> Optional[DamageFormulaContext]:
        return self._eval_effect(char, state)

    def __eq__(self, other):
        if isinstance(other, WorldFlipperAbility):
            return self.name == other.name
        return False
