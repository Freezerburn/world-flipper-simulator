from wfdata.wfjson.wfjson import WfJson
from typing import Literal
import pprint
import deepdiff


EffectEnum = Literal[
    "main_effect", "main_condition", "continuous_effect", "continuous_condition"
]


# TODO: Figure out if continuous effect 45 always has 2 as the direct hits count.
# See: brown_fighter_3 (Sonia)
# I don't see a count anywhere in the data structure to indicate number of direct
# hits, so it seems like that number might be hard-coded right now.
# TODO: Figure out how "Poisoned" gets passed to effect 510.
# See: onmyoji_boy_2 (Water Suizen), which has the condition of applying the buff
# when the foe is Poisoned. Nothing obvious in the ability shows up when I saw
# it the first time. Have to find someone else with it to see if I can find a
# difference in the ability data.
def diff_effect(effect_type: EffectEnum, effect_index: str):
    wf_json = WfJson("wf_data_json")
    effects = []
    for char in wf_json.characters.values():
        for ab_effects in char.abilities:
            for ab in ab_effects:
                if effect_type == "main_effect":
                    if ab.main_effect_index == effect_index:
                        effects.append(ab)
                elif effect_type == "main_condition":
                    if ab.main_condition_index == effect_index:
                        effects.append(ab)
                elif effect_type == "continuous_effect":
                    if ab.continuous_effect_index == effect_index:
                        effects.append(ab)
                elif effect_type == "continuous_condition":
                    if ab.continuous_condition_index == effect_index:
                        effects.append(ab)

    if len(effects) < 2:
        return
    base = effects[0]
    for other in effects[1:]:
        dd = deepdiff.diff.DeepDiff(base, other)["values_changed"]
        for ignore in [
            "root.name",
            "root.ability_statue_group",
            "root.main_effect_min",
            "root.main_effect_max",
            "root.is_main",
        ]:
            if ignore in dd:
                del dd[ignore]
        if len(dd) == 0:
            continue
        pprint.pprint(dd)


def list_main_effect_indices():
    wf_json = WfJson("wf_data_json")
    indices = set()
    for char in wf_json.characters.values():
        for ab_effects in char.abilities:
            for ab in ab_effects:
                if ab.effect_type != "0":
                    continue
                indices.add(ab.main_effect_index)
    print(f"Total Main Effect indices: {len(indices)}")
    idx_l = list(indices)
    idx_l.sort()
    output = {}
    for idx in idx_l:
        output[idx] = []
    pprint.pprint(output)


# noinspection PyBroadException
def debug_unknown_effect_indices():
    wf_json = WfJson("wf_data_json")
    unknown_idxs = set()
    unknowns = set()
    for char in wf_json.characters.values():
        for ab_effects in char.abilities:
            for ab in ab_effects:
                try:
                    ab.main_effect_ui()
                except:
                    unknown_idxs.add(ab.main_effect_index)
                    unknowns.add((char.name, ab.name, ab.main_effect_index))
    unknown_l = list(unknowns)
    unknown_l.sort(key=lambda l: l[2])
    print(f"Not yet handled main effects: {len(unknown_idxs)}")
    for char_name, ab_name, idx in unknown_l:
        print(f"MAIN EFFECT: {char_name:>24} | {ab_name:30} | {idx:4}")


def main():
    # debug_unknown_effect_indices()
    # list_main_effect_indices()
    diff_effect("main_effect", "156")


if __name__ == "__main__":
    main()
