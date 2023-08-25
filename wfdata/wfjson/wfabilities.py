from typing import LiteralString

main_effect_mapping: dict[str, list[str]] = {
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


class AbilityJson:
    def __init__(self, data):
        self.name = data[0]
        self.is_main = data[1] == "true"
        self.ability_statue_group = data[2]
        self.effect_type: LiteralString["0", "1"] = data[
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

    # 0: this unit
    # 1: all other allied units
    # 2: Leader
    # 5: All(?)/elemental unit
    # 7: Unit that triggered the condition
    # 8: Multiballs
    def target_index_friendly(self, target, element=None):
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

    def main_condition_ui(self):
        if self.effect_type != "0":
            return "(None)"
        if (
            self.main_condition_index not in main_effect_mapping
            or len(main_effect_mapping[self.main_condition_index]) == 0
        ):
            raise RuntimeError(
                f"[{self.name}] Unknown main condition index: {self.main_condition_index}"
            )

        return main_effect_mapping[self.main_condition_index]

    def main_effect_ui(self) -> list[str]:
        if self.effect_type != "0":
            return []

        if self.main_effect_index == "0":
            return [
                "ability_description_for_second",
                "ability_description_common_content_attack",
            ]
        elif self.main_effect_index == "26":
            return [
                "ability_description_for_second",
                "ability_description_condition_content_piercing",
            ]
        elif self.main_effect_index == "28":
            return [
                "ability_description_for_second",
                "ability_description_common_content_power_flip_damage",
            ]
        elif self.main_effect_index == "31":
            return ["ability_description_common_content_attack"]
        elif self.main_effect_index == "33":
            return ["ability_description_common_content_skill_damage"]
        elif self.main_effect_index == "49":
            return ["ability_description_common_content_fever_point"]
        elif self.main_effect_index == "54":
            return ["ability_description_common_content_power_flip_damage"]
        elif self.main_effect_index == "152":
            return ["ability_description_common_content_power_flip_damage_lv"]
        elif self.main_effect_index == "156":
            return ["ability_description_common_content_condition_extend"]
        elif self.main_effect_index == "198":
            return ["ability_description_common_content_power_flip_combo_count_down"]
        elif self.main_effect_index == "203":
            return ["ability_description_instant_content_hp"]
        elif self.main_effect_index == "209":
            return ["ability_description_instant_content_skill_gauge"]
        elif self.main_effect_index == "510":
            return ["ability_description_common_content_condition_slayer"]
        else:
            raise RuntimeError(
                f"[{self.name}] Unknown main effect index: {self.main_effect_index}"
            )

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
            return (
                "ability_description_common_content_aditional_direct_attack_and_damage"
            )
        else:
            raise RuntimeError(
                f"[{self.name}] Unknown continuous index: {self.continuous_effect_index}"
            )
