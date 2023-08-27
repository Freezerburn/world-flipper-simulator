from typing import Literal
from .wfdmgformula import DamageFormulaContext
from .wfenum import CharPosition


_main_condition_mapping: dict[str, list[str]] = {
    "0": ["ability_description_instant_trigger_kind_first_flip"],
    "1": [
        "ability_description_n_times",
        "ability_description_instant_trigger_kind_power_flip",
    ],
    "100": [
        "ability_description_n_times",
        "ability_description_instant_trigger_kind_skill_hit",
    ],
    "13": [],
    "131": [],
    "132": [],
    "136": [],
    "137": [],
    "14": [],
    "15": [],
    "16": [],
    "18": ["ability_description_instant_trigger_kind_skill_invoke"],
    "19": [],
    "2": [],
    "20": [],
    "22": [],
    "23": [],
    "24": [],
    "3": [
        "ability_description_n_times",
        "ability_description_instant_trigger_kind_ball_flip",
    ],
    "4": ["ability_description_instant_trigger_kind_fever"],
    "45": [],
    "46": [],
    "5": [],
    "50": [],
    "51": [],
    "56": [],
    "57": [],
    "58": [],
    "59": [],
    "6": ["ability_description_instant_trigger_kind_enemy_kill"],
    "63": [],
    "7": ["ability_description_instant_trigger_kind_combo"],
    "70": [],
    "8": [],
}

_main_effect_mapping: dict[str, list[str]] = {
    "0": [
        "ability_description_for_second",
        "ability_description_common_content_attack",
    ],
    "1": [],
    "112": [],
    "116": [],
    "117": [],
    "118": [],
    "123": [],
    "144": [],
    "152": ["ability_description_common_content_power_flip_damage_lv"],
    "155": [],
    # NOTE: This ALWAYS sets "Attack Buff" as the condition.
    "156": ["ability_description_common_content_condition_extend"],
    "158": [],
    "16": [],
    "162": [],
    "164": [],
    "17": [],
    "176": [],
    "189": [],
    "190": [],
    "191": [],
    "193": [],
    "195": [],
    "196": [],
    "198": ["ability_description_common_content_power_flip_combo_count_down"],
    "199": [],
    "2": [],
    "201": [],
    "203": ["ability_description_instant_content_hp"],
    "204": [],
    "207": [],
    "209": ["ability_description_instant_content_skill_gauge"],
    "21": [],
    "211": [],
    "212": [],
    "218": [],
    "221": [],
    "222": [],
    "224": [],
    "225": [],
    "24": [],
    "243": [],
    "245": [],
    "249": [],
    "251": [],
    "253": [],
    "26": [
        "ability_description_for_second",
        "ability_description_condition_content_piercing",
    ],
    "265": [],
    "27": [],
    "28": [
        "ability_description_for_second",
        "ability_description_common_content_power_flip_damage",
    ],
    "289": [],
    "307": [],
    "31": ["ability_description_common_content_attack"],
    "32": [],
    "33": ["ability_description_common_content_skill_damage"],
    "330": [],
    "34": [],
    "35": [],
    "354": [],
    "36": [],
    "366": [],
    "37": [],
    "38": [],
    "386": [],
    "388": [],
    "389": [],
    "39": [],
    "391": [],
    "4": [],
    "40": [],
    "41": [],
    "411": [],
    "459": [],
    "460": [],
    "466": [],
    "468": [],
    "487": [],
    "489": [],
    "49": ["ability_description_common_content_fever_point"],
    "5": [],
    "50": [],
    "501": [],
    "503": [],
    "504": [],
    "505": [],
    "506": [],
    "51": [],
    "510": ["ability_description_common_content_condition_slayer"],
    "512": [],
    "518": [],
    "52": [],
    "522": [],
    "525": [],
    "533": [],
    "54": ["ability_description_common_content_power_flip_damage"],
    "55": [],
    "58": [],
    "61": [],
    "66": [],
    "67": [],
    "68": [],
    "69": [],
    "7": [],
    "8": [],
    "95": [],
    "98": [],
}

_COUNT_CONVERT = 100_000
_SEC_CONVERT = 600_000


def _leader(party: list):
    for c in party:
        if c.position == CharPosition.LEADER:
            return c
    raise RuntimeError(f"Invalid party state: No Leader!")


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
    applied. The JSON stores the multiplier/total number of times it can be triggered in the JSON so we can
    use that directly to make sure that we don't go over it.
    :param lv: The current level of the ability.
    :param count: The number of times the condition for an ability has been triggered.
    :return:
    """
    v_min = u_min / conv
    v_max = u_max / conv
    step = abs(v_max - v_min) / 5
    req = v_min + step * (lv - 1)
    times = count / req
    if times >= cap:
        times = cap
    return times


class WorldFlipperAbility:
    def __init__(self, data, from_char):
        self.from_char = from_char
        self.name = data[0]
        self.is_main = data[1] == "true"
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
        self.effect_target_element = data[32]
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
        self.continuous_cooldown_time = data[66]  # TODO: Verify
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

    def main_condition_ui(self) -> list[str]:
        if self.effect_type != "0":
            return []
        if (
            self.main_condition_index not in _main_condition_mapping
            or len(_main_condition_mapping[self.main_condition_index]) == 0
        ):
            raise RuntimeError(
                f"[{self.name}] Unknown main condition index: {self.main_condition_index}"
            )
        return _main_condition_mapping[self.main_condition_index]

    def main_effect_ui(self) -> list[str]:
        if self.effect_type != "0":
            return []
        if (
            self.main_effect_index not in _main_effect_mapping
            or len(_main_effect_mapping[self.main_effect_index]) == 0
        ):
            raise RuntimeError(
                f"[{self.name}] Unknown main condition index: {self.main_effect_index}"
            )
        return _main_effect_mapping[self.main_effect_index]

    def continuous_condition_ui(self):
        if self.effect_type != "1":
            return "(None)"

        if self.continuous_condition_index == "5":
            return "ability_description_during_trigger_kind_multiball"
        elif self.continuous_condition_index == "8":
            return "ability_description_during_trigger_kind_condition"
        else:
            raise RuntimeError(
                f"[{self.name}] Unknown continuous condition: {self.continuous_condition_index}"
            )

    def continuous_effect_ui(self):
        if self.effect_type != "1":
            return "(None)"

        if self.continuous_effect_index == "0":
            return "ability_description_common_content_attack"
        elif self.continuous_effect_index == "45":
            # NOTE: Direct hits number (so far) is always hardcoded to 2.
            return (
                "ability_description_common_content_aditional_direct_attack_and_damage"
            )
        else:
            raise RuntimeError(
                f"[{self.name}] Unknown continuous index: {self.continuous_effect_index}"
            )

    def _apply_main_effect(
        self, ui_name: list[str], ctx: DamageFormulaContext, times=1
    ):
        pass

    def eval_main_effect(
        self, lv: int, char, enemy, party: list
    ) -> DamageFormulaContext | None:
        ret = DamageFormulaContext(char, enemy)
        if self.effect_type != "0":
            return None
        if char.position is None:
            return None
        if lv == 0:
            return None

        condition_ui_name = self.main_condition_ui()
        effect_ui_name = self.main_effect_ui()

        match condition_ui_name[0]:
            case "ability_description_instant_trigger_kind_first_flip":
                # Apply effect at battle start, so it's always active.
                self._apply_main_effect(effect_ui_name, ret)
                return ret

            case "ability_description_n_times":
                # Condition requires something to happen a number of times, so we need to check the second
                # element in the list to figure out what to count, and then check how many times that thing
                # has happened to see if it currently applies.
                if len(condition_ui_name) == 1:
                    raise RuntimeError(
                        f"[{char.name}] Ability index {self.main_condition_index} had count condition, but nothing to count."
                    )

                match condition_ui_name[1]:
                    case "ability_description_instant_trigger_kind_power_flip":
                        times = _calc_req_units(
                            int(self.main_condition_min),
                            int(self.main_condition_max),
                            _COUNT_CONVERT,
                            int(self.main_effect_max_multiplier),
                            lv,
                            _leader(party).total_power_flips,
                        )
                        self._apply_main_effect(effect_ui_name, ret, times=times)
                        return ret
                    case "ability_description_instant_trigger_kind_skill_hit":
                        times = _calc_req_units(
                            int(self.main_condition_min),
                            int(self.main_condition_max),
                            _COUNT_CONVERT,
                            int(self.main_effect_max_multiplier),
                            lv,
                            char.total_skill_hits,
                        )
                        self._apply_main_effect(effect_ui_name, ret, times=times)
                        return ret

        return ret
