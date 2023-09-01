from __future__ import annotations
from typing import Literal, Optional, TYPE_CHECKING

import math

from .wfabilitymapping import (
    _continuous_condition_mapping,
    _continuous_effect_mapping,
)
from .wfdmgformula import DamageFormulaContext
from .wfenum import CharPosition, Element, Debuff
from .wfgamestate import GameState

from .wfeffects.wfeffect import EffectParams
from .wfeffects.wfmaineffectmapping import main_condition_mapping, main_effect_mapping

if TYPE_CHECKING:
    from .wfchar import WorldFlipperCharacter

_PERCENT_CONVERT = 100_000
_COUNT_CONVERT = 100_000
_SEC_CONVERT = 600_000

# TODO: Going to need something that can evaluate an ability to figure out what UI elements to show.
# Not all abilities are going to need a toggle to say whether or not they're going to be active, as
# an example. Things that might need this would be stuff like a continuous effect that has a
# condition for when the effect is going to be applied. Or showing a slider or something for when
# something requires a certain number of powerflips so that the user can decide what level of buff
# is currently active for the purposes of calculations.


def _leader(party: list):
    for c in party:
        if c.position == CharPosition.LEADER:
            return c
    raise RuntimeError(f"Invalid party state: No Leader!")


def _calc_abil_lv(u_min: int, u_max: int, conv: int, lv: int) -> float:
    v_min = u_min / conv
    v_max = u_max / conv
    step = abs(v_max - v_min) / 5
    return v_min + step * (lv - 1)


def _calc_req_units(
    u_min: int, u_max: int, conv: int, cap: int, lv: int, count: int
) -> int:
    """
    Abilities generally have a linear increment on each level they gain on the mana board between a minimum
    and a maximum. This calculates the current value for an ability based on its current level.
    :param u_min: The minimum value of an ability/condition.
    :param u_max: The maximum value of an ability/condition.
    :param conv: What the min/max value needs to be divided by in order to turn it into how it will be used
    in calculations/displayed in the UI. As an example: When an ability mentions "every N power flips", the
    JSON stores N * 100,000. So "every 5 power flips" would be stored as 500000.
    :param cap: Every ability that can be triggered multiple times has a limit on how many times it can be
    applied. The JSON stores the multiplier/total number of times it can be triggered in the JSON, so we can
    use that directly to make sure that we don't go over it.
    :param lv: The current level of the ability.
    :param count: The number of times the condition for an ability has been triggered.
    :return:
    """
    req = _calc_abil_lv(u_min, u_max, conv, lv)
    times = math.floor(count / req)
    if times >= cap:
        times = cap
    return times


class EffectParameters:
    def __init__(self, idx: str, target: str, element: str, min_v: str, max_v: str):
        self.idx = idx
        self.target = target
        self.element = element
        self.min_v = min_v
        self.max_v = max_v


class WorldFlipperAbility:
    def __init__(self, data, from_char):
        self.from_char = from_char
        self.name = data[0]
        self.requires_main = data[1] == "false"
        self.ability_statue_group = data[2]
        self.effect_type: Literal["0", "1"] = data[
            3
        ]  # 0 for "main effect", 1 for continuous
        self.party_condition_index = data[4]  # TODO: Verify
        self.slot5 = data[5]
        self.slot6 = data[6]
        self.slot7 = data[7]
        self.slot8 = data[8]
        self.party_condition_element = data[9]  # TODO: Verify
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
        self.main_condition_element = data[27]
        self.main_condition_min = data[28]
        self.main_condition_max = data[29]
        # Valid values:
        # ""
        # "<number>"
        # "(None)"
        self.main_effect_max_multiplier = data[30]
        self.cooldown_time = data[31]  # Seconds multiplied by 60.
        self.condition_target_element = data[32]
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
        self.main_effect_element = data[44]
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
        self.continuous_condition_element = data[63]
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
        self.continuous_effect_element = data[75]
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

    def element_enum(self, element):
        match element:
            case "Red":
                return Element.FIRE
            case "Yellow":
                return Element.THUNDER
            case "Green":
                return Element.WIND
            case "Blue":
                return Element.WATER
            case "White":
                return Element.LIGHT
            case "Black":
                return Element.DARK
            case _:
                return None

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

    def main_condition_ui(self) -> list[str]:
        if self.effect_type != "0":
            return []
        if (
            self.main_condition_index not in main_condition_mapping
            or main_condition_mapping[self.main_condition_index] is None
        ):
            raise RuntimeError(
                f"[{self.name}] Unknown main condition index: {self.main_condition_index}"
            )
        return main_condition_mapping[self.main_condition_index].ui_key()

    def main_effect_ui(self) -> list[str]:
        if self.effect_type != "0":
            return []
        if (
            self.main_effect_index not in main_effect_mapping
            or len(main_effect_mapping[self.main_effect_index]) == 0
        ):
            raise RuntimeError(
                f"[{self.name}] Unknown main effect index: {self.main_effect_index}"
            )
        ret = []
        for e in main_effect_mapping[self.main_effect_index]:
            for key in e.ui_key():
                ret.append(key)
        return ret

    def continuous_condition_ui(self):
        if self.is_main_effect():
            return None
        if self.continuous_condition_index not in _continuous_condition_mapping:
            raise RuntimeError(
                f"[{self.name}] Unknown continuous condition: {self.continuous_condition_index}"
            )
        return _continuous_condition_mapping[self.continuous_condition_index]

    def continuous_effect_ui(self):
        if self.is_main_effect():
            return None
        if self.continuous_effect_index not in _continuous_effect_mapping:
            raise RuntimeError(
                f"[{self.name} Unknown continuous effect index: {self.continuous_effect_index}"
            )
        return _continuous_effect_mapping[self.continuous_effect_index]

    def _target_applies_to(
        self, target: str, element: str, char: WorldFlipperCharacter
    ) -> bool:
        match target:
            case "":
                return True
            case "0":
                return self.from_char.internal_name == char.internal_name
            case "1":
                return self.from_char.internal_name != char.internal_name
            case "2":
                return char.position == CharPosition.LEADER
            case "5" | "7":
                if not element:
                    return True
                else:
                    return char.element == self.element_enum(element)
            case "8":
                # TODO: Implement multiball
                return False

        return False

    def _apply_main_effect(
        self,
        ui_name: list[str],
        ctx: DamageFormulaContext,
        state: GameState,
        times=1,
    ):
        char_idx, ab_idx = state.ability_index(self)
        lv = state.ability_lvs[char_idx][ab_idx]
        match ui_name[0]:
            case "ability_description_for_second":
                if not state.ability_condition_active[char_idx][ab_idx]:
                    return
                self._apply_main_effect(ui_name[1:], ctx, state, times=times)

            case "ability_description_common_content_attack":
                amt = _calc_abil_lv(
                    int(self.main_effect_min),
                    int(self.main_effect_max),
                    _PERCENT_CONVERT,
                    lv,
                )
                ctx.attack_modifier += amt * times

            case "ability_description_common_content_power_flip_damage":
                if state.position(ctx.char) != CharPosition.LEADER:
                    ctx.valid = False
                    return
                amt = _calc_abil_lv(
                    int(self.main_effect_min),
                    int(self.main_effect_max),
                    _PERCENT_CONVERT,
                    lv,
                )
                ctx.stat_mod_pf_damage += amt * times

            case "ability_description_common_content_power_flip_damage_lv":
                amt = _calc_abil_lv(
                    int(self.main_effect_min),
                    int(self.main_effect_max),
                    _PERCENT_CONVERT,
                    lv,
                )
                ctx.stat_mod_pf_lv_damage_slayer += amt * times
                ctx.stat_mod_pf_lv_damage_slayer_lv = 3

            case "ability_description_common_content_skill_damage":
                amt = _calc_abil_lv(
                    int(self.main_effect_min),
                    int(self.main_effect_max),
                    _PERCENT_CONVERT,
                    lv,
                )
                ctx.stat_mod_sd_damage += amt * times

            case "ability_description_common_content_condition_slayer":
                amt = _calc_abil_lv(
                    int(self.main_effect_min),
                    int(self.main_effect_max),
                    _PERCENT_CONVERT,
                    lv,
                )
                if state.enemy is None:
                    return
                try:
                    state.enemy.debuffs.index(Debuff.FIRE_RESISTANCE)
                    ctx.condition_slayer += amt
                except ValueError:
                    pass

            case "ability_description_common_content_second_skill_gauge":
                ctx.skill_gauge_max[char_idx] = 200

            case "ability_description_instant_content_skill_gauge":
                amt = _calc_abil_lv(
                    int(self.main_effect_min),
                    int(self.main_effect_max),
                    _PERCENT_CONVERT,
                    lv,
                )
                ctx.skill_charge[state.main_index(char_idx)] += amt

            case "ability_description_common_content_power_flip_combo_count_down":
                ctx.pf_combo_reduction[2] += 5

            case "ability_description_instant_content_enemy_damage":
                # This does instant damage when a skill is invoked, so there's nothing to really
                # do in the simulator.
                # Just mark it as invalid so nothing gets returned.
                ctx.valid = False

            case _:
                raise RuntimeError(
                    f"[{self.name}] Failed to apply main effect: {ui_name}"
                )

    def _eval_main_effect(
        self,
        char: WorldFlipperCharacter,
        state: GameState,
    ) -> Optional[DamageFormulaContext]:
        condition_ui = self.main_condition_ui()
        effect_ui = self.main_effect_ui()

        if self.main_condition_index not in main_condition_mapping:
            raise RuntimeError(
                f"[{self.name}] Unknown main condition: {self.main_condition_index}"
            )
        if self.main_effect_index not in main_effect_mapping:
            raise RuntimeError(
                f"[{self.name}] Unknown main effect: {self.main_effect_index}"
            )

        ab_char_idx, _ = state.ability_index(self)
        ctx = DamageFormulaContext()
        condition_param = EffectParams(
            condition_ui, self, state, char, state.party[ab_char_idx], ctx
        )
        effect_param = EffectParams(
            effect_ui, self, state, char, state.party[ab_char_idx], ctx
        )

        condition = main_condition_mapping[self.main_condition_index](condition_param)

        if not condition.should_run():
            return None
        if not condition.eval():
            return None
        effect_param.multiplier = condition.multiplier
        for e in main_effect_mapping[self.main_effect_index]:
            if not e(effect_param).eval():
                return None
        return effect_param.ctx

    def _apply_continuous_effect(
        self,
        ui_name: list[str],
        ctx: DamageFormulaContext,
        state: GameState,
        times=1,
    ):
        char_idx, ab_idx = state.ability_index(self)
        lv = state.ability_lvs[char_idx][ab_idx]
        match ui_name[0]:
            case "ability_description_common_content_skill_gauge_chaging":
                amt = _calc_abil_lv(
                    int(self.continuous_effect_min),
                    int(self.continuous_effect_max),
                    _COUNT_CONVERT,
                    lv,
                )
                ctx.skill_charge_speed[char_idx] += amt

            case "ability_description_common_content_direct_damage":
                amt = _calc_abil_lv(
                    int(self.continuous_effect_min),
                    int(self.continuous_effect_max),
                    _COUNT_CONVERT,
                    lv,
                )
                ctx.stat_mod_da_damage += amt * times

            case "ability_description_common_content_attack":
                amt = _calc_abil_lv(
                    int(self.continuous_effect_min),
                    int(self.continuous_effect_max),
                    _COUNT_CONVERT,
                    lv,
                )
                ctx.attack_modifier += amt * times

    # TODO: Implement
    def _eval_continuous_effect(
        self, char: WorldFlipperCharacter, state: GameState
    ) -> Optional[DamageFormulaContext]:
        if self.is_main_effect():
            return None
        position = state.position(char)
        if position is None:
            return None
        char_idx = state.party.index(char)
        ab_char_idx, ab_idx = state.ability_index(self)
        if ab_char_idx == -1:
            return None
        lv = state.ability_lvs[ab_char_idx][ab_idx]
        if lv == 0:
            return None
        # Don't apply an effect if it requires a character to be in a main slot and the unit is
        # a unison.
        if (
            self.requires_main
            and state.position(state.party[ab_char_idx]) == CharPosition.UNISON
        ):
            return None
        if not self._target_applies_to(
            self.continuous_effect_target, self.continuous_effect_element, char
        ):
            return None

        ret = DamageFormulaContext()
        condition_ui_name = self.continuous_condition_ui()
        effect_ui_name = self.continuous_effect_ui()
        match condition_ui_name[0]:
            case "ability_description_during_trigger_kind_multiball":
                amt = _calc_abil_lv(
                    int(self.continuous_condition_min),
                    int(self.continuous_condition_max),
                    _COUNT_CONVERT,
                    lv,
                )
                if state.num_multiballs >= amt:
                    self._apply_continuous_effect(effect_ui_name, ret, state)

            case "ability_description_during_trigger_kind_condition":
                pass

            case "ability_description_during_trigger_kind_skill_gauge_high":
                amt = _calc_abil_lv(
                    int(self.continuous_condition_min),
                    int(self.continuous_condition_max),
                    _COUNT_CONVERT,
                    lv,
                )
                target_char_idx = -1
                match self.continuous_effect_target:
                    case "0":
                        target_char_idx = ab_char_idx
                    case "7":
                        target_char_idx = char_idx
                    case _:
                        raise RuntimeError(
                            f"[{condition_ui_name[0]}] Unhandled continuous "
                            f"target: {self.continuous_effect_target}"
                        )
                if state.skill_charge[target_char_idx] <= amt:
                    return None
                self._apply_continuous_effect(effect_ui_name, ret, state)

            case "ability_description_during_trigger_kind_one_of_enemy_condition_high_count":
                element = self.element_enum(self.continuous_effect_element)
                if element is not None and char.element != element:
                    return None
                times = _calc_req_units(
                    int(self.continuous_condition_min),
                    int(self.continuous_condition_max),
                    _COUNT_CONVERT,
                    int(self.continuous_effect_max_multiplier),
                    lv,
                    len(state.enemy.debuffs),
                )
                self._apply_continuous_effect(effect_ui_name, ret, state, times=times)

        if not ret.valid:
            return None
        return ret

    # TODO: Should probably create an "eval context" kind of thing for holding artifical state from user.
    # Basically the thing that holds all the info a user would be able to set up for figuring out damage
    # numbers, such as how many power flips have happened so far, skill hits, balls being launched, party
    # composition, ability levels, etc.
    # That can hopefully help prevent having a huge amount of data being put directly into somewhere like
    # a character, and instead isolate the UI setup into its own distinct area that can then be used
    # during eval.
    # Should also hopefully help prevent an explosion of parameters from being sent to the eval functions
    # as well.
    def eval_effect(
        self,
        char: WorldFlipperCharacter,
        state: GameState,
    ) -> Optional[DamageFormulaContext]:
        if self.is_main_effect():
            return self._eval_main_effect(char, state)
        else:
            return self._eval_continuous_effect(char, state)

    def __eq__(self, other):
        if isinstance(other, WorldFlipperAbility):
            return self.name == other.name
        return False
