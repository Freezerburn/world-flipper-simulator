def _condition_effect(data):
    key = data[25]
    if key == "0":
        return "ability_description_instant_trigger_kind_first_flip"
    elif key == "18":
        return "ability_description_instant_trigger_kind_skill_invoke"


def _one_argument_effect(data):
    key = data[42]
    if key == "31":
        return "ability_description_common_content_attack"
    elif key == "33":
        return "ability_description_common_content_skill_damage"
    elif key == "203":
        return "ability_description_instant_content_hp"
    elif key == "209":
        return "ability_description_instant_content_skill_gauge"
    else:
        raise RuntimeError(f"Unknown unconditional_id: {key}")


def _two_argument_effect(data):
    pass


def ability_to_ui(data):
    condition_id = data[25]
    condition = None
    if condition_id:
        condition = _condition_effect(data)

    base_effect_kind = data[3]
    base_effect = None
    if base_effect_kind == "0":
        base_effect = _one_argument_effect(data)
    elif base_effect_kind == "1":
        base_effect = _two_argument_effect(data)
    else:
        raise RuntimeError(f"Unknown conditional_id: {base_effect_kind}")

    ret = []
    if condition:
        ret.append(condition)
    if base_effect:
        ret.append(base_effect)
    return ret
