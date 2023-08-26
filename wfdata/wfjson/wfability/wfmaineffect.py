from wfdata.wfdmgformula import DamageFormulaContext
from wfdata.wfenum import CharPosition

main_condition_mapping: dict[str, list[str]] = {
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


def _leader(party: list):
    for c in party:
        if c.position == CharPosition.LEADER:
            return c
    raise RuntimeError(f"Invalid party state: No Leader!")


def main_condition_ui(idx: str, name=None) -> list[str]:
    if idx not in main_condition_mapping or len(main_condition_mapping[idx]) == 0:
        if name is not None:
            raise RuntimeError(f"Unknown main condition index: {idx}")
        else:
            raise RuntimeError(f"[{name}] Unknown main condition index: {idx}")
    return main_condition_mapping[idx]


def main_effect_ui(idx: str, name=None) -> list[str]:
    if idx not in main_effect_mapping or len(main_effect_mapping[idx]) == 0:
        if name is not None:
            raise RuntimeError(f"Unknown main effect index: {idx}")
        else:
            raise RuntimeError(f"[{name}] Unknown main effect index: {idx}")
    return main_effect_mapping[idx]


def _apply_main_effect(ui_name: list[str], ctx: DamageFormulaContext, times=1):
    pass


def eval_main_effect(
    ability, lv: int, char, enemy, party: list
) -> DamageFormulaContext | None:
    ret = DamageFormulaContext(char, enemy)
    if ability.effect_type != "0":
        return None
    if char.position is None:
        return None
    if lv == 0:
        return None

    condition_ui_name = main_condition_ui(ability.main_condition_index, name=char.name)
    effect_ui_name = main_effect_ui(ability.main_effect_index, name=char.name)
    c_ab1 = condition_ui_name[0]

    # Apply effect at battle start, so it's always active.
    if c_ab1 == "ability_description_instant_trigger_kind_first_flip":
        _apply_main_effect(effect_ui_name, ret)
        return ret

    # Condition requires something to happen a number of times, so we need to check the second
    # element in the list to figure out what to count, and then check how many times that thing
    # has happened to see if it currently applies.
    if c_ab1 == "ability_description_n_times":
        if len(condition_ui_name) == 1:
            raise RuntimeError(
                f"[{char.name}] Ability index {ability.main_condition_index} had count condition, but nothing to count."
            )

        c_ab2 = condition_ui_name[1]
        if c_ab2 == "ability_description_instant_trigger_kind_power_flip":
            min_pfs = ability.main_condition_min / 100000
            max_pfs = ability.main_condition_max / 100000
            pfs_step = abs(max_pfs - min_pfs) / 5
            req_pfs = min_pfs + pfs_step * (lv - 1)
            times = _leader(party).total_power_flips / req_pfs
            times_cap = int(ability.main_effect_max_multiplier)
            if times >= times_cap:
                times = times_cap
            _apply_main_effect(effect_ui_name, ret, times=times)
            return ret

    return ret
