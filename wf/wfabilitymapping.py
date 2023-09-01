_continuous_condition_mapping: dict[str, list[str]] = {
    "5": ["ability_description_during_trigger_kind_multiball"],
    "8": ["ability_description_during_trigger_kind_condition"],
    "105": ["ability_description_during_trigger_kind_skill_gauge_high"],
    # NOTE: Condition is always hardcoded as Debuff.
    "134": [
        "ability_description_during_trigger_kind_one_of_enemy_condition_high_count"
    ],
}

_continuous_effect_mapping: dict[str, list[str]] = {
    "0": ["ability_description_common_content_attack"],
    "3": ["ability_description_common_content_skill_gauge_chaging"],
    # NOTE: Direct hits number (so far) is always hardcoded to 2.
    "45": ["ability_description_common_content_aditional_direct_attack_and_damage"],
    "159": ["ability_description_common_content_direct_damage"],
    "258": ["ability_description_common_content_attack"],
}
