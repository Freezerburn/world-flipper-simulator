import json
from wfdata.wfenum import PowerFlip, Element
from wfdata.wfjson.wfabilities import AbilityJson


class WfJsonCharacter:
    def __init__(self, key, data):
        self.id = key
        data_arr = data[0]
        self.internal_name = data_arr[0]
        self.races = data_arr[4].split(",")
        self.gender = data_arr[7]
        self.leader_skill_name = data_arr[10]
        self.stars = int(data_arr[2])
        self.ability_ids = data_arr[11:16]
        self.abilities: list[list[AbilityJson]] = []

        pf_id = data_arr[6]
        if pf_id == "0":
            self.pf_type = PowerFlip.SWORD
        elif pf_id == "1":
            self.pf_type = PowerFlip.FIST
        elif pf_id == "2":
            self.pf_type = PowerFlip.BOW
        elif pf_id == "3":
            self.pf_type = PowerFlip.SUPPORT
        elif pf_id == "4":
            self.pf_type = PowerFlip.SPECIAL

        element_id = data_arr[3]
        if element_id == "0":
            self.element = Element.FIRE
        elif element_id == "1":
            self.element = Element.WATER
        elif element_id == "2":
            self.element = Element.THUNDER
        elif element_id == "3":
            self.element = Element.WIND
        elif element_id == "4":
            self.element = Element.LIGHT
        elif element_id == "5":
            self.element = Element.DARK

        self.name = None
        self.base_atk = 0
        self.base_hp = 0
        self.skill_name = None
        self.skill_name_evolve = None
        self.skill_base_dmg = 0
        self.skill_base_cost = 0
        self.skill_evolve_cost = 0

    def __str__(self):
        return (
            f"{self.name} ({self.id} | {self.internal_name})\n"
            f"ATK:{self.base_atk} | HP:{self.base_hp}\n"
            f"Skill: {self.skill_name} (Evolve: {self.skill_name_evolve})\n"
            f"Skill DMG:{self.skill_base_dmg} | COST:{self.skill_base_cost} (Evolve COST:{self.skill_evolve_cost})"
        )


class WfJson:
    def __init__(self, data_dir):
        self.characters = {}
        self.characters_by_internal_name = {}
        self.characters_by_name = {}

        # Most of the base data/attributes of any individual character. Stuff like stars, power flip type, element, etc.
        with open(f"{data_dir}/character/character.json", "r") as f:
            character_json = json.load(f)
        # Holds a bunch of user-facing description text, most importantly for our purposes: The name.
        with open(f"{data_dir}/character/character_text.json", "r") as f:
            character_text_json = json.load(f)
        # Character status file purely includes the atk/hp curves for characters.
        # The level 10 entry for each character (keyed on their ID) is the "base" atk/hp
        # for that character.
        with open(f"{data_dir}/character/character_status.json", "r") as f:
            character_status_json = json.load(f)
        # Action skills use the "internal name" of a character as the key to access
        # their info.
        with open(f"{data_dir}/skill/action_skill.json", "r") as f:
            action_skill_json = json.load(f)
        with open(f"{data_dir}/ability/ability.json", "r") as f:
            abilities_json = json.load(f)

        for key in character_json:
            char = WfJsonCharacter(key, character_json[key])
            char.name = character_text_json[char.id][0][0]
            char.base_atk = int(character_status_json[char.id]["10"][0][0])
            char.base_hp = int(character_status_json[char.id]["10"][0][1])

            action_skill = action_skill_json[char.internal_name]
            base_skill = action_skill["1"][0]
            char.skill_name = base_skill[0]
            char.skill_base_cost = int(base_skill[5])
            if base_skill[10]:
                char.skill_base_dmg = int(base_skill[10])

            if "2" in action_skill:
                evolve_skill = action_skill["2"][0]
                char.skill_name_evolve = evolve_skill[0]
                char.skill_evolve_cost = int(evolve_skill[5])

            for ability_id in char.ability_ids:
                if ability_id == "(None)":
                    continue
                ability_json = abilities_json[ability_id]
                effects = []
                for ability_effect_json in ability_json:
                    effects.append(AbilityJson(ability_effect_json))
                char.abilities.append(effects)

            self.characters[char.id] = char
            self.characters_by_internal_name[char.internal_name] = char
            self.characters_by_name[char.name] = char

    def find(self, key):
        if key in self.characters:
            return self.characters[key]
        elif key in self.characters_by_internal_name:
            return self.characters_by_internal_name[key]
        elif key in self.characters_by_name:
            return self.characters_by_name[key]
        raise IndexError(f"No character with key {key} in database.")
