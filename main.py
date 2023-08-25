from wfdata.wfjson.wfjson import WfJson


def main():
    wf_json = WfJson("wf_data_json")
    print(wf_json.find("Beaucy"))

    for char in wf_json.characters.values():
        for ab_effects in char.abilities:
            print(f"CHAR [{char.name}] ABILITIES")
            for ab in ab_effects:
                print(f"EFFECT [{ab.name}]")
                print(f"  MAIN CONDITION :: {ab.main_condition_ui()}")
                print(f"  MAIN EFFECT :: {ab.main_effect_ui()}")

                print(f"  CONTINUOUS CONDITION :: {ab.continuous_condition_ui()}")
                print(f"  CONTINUOUS EFFECT :: {ab.continuous_effect_ui()}")


if __name__ == "__main__":
    main()
