import json


class WfJsonCharacter:
    def __init__(self, key, data):
        self.id = key
        data_arr = data[0]
        self.internal_name = data_arr[0]
        self.races = data_arr[4].split(",")
        self.gender = data_arr[7]
        self.leader_skill_name = data_arr[10]

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

        with open(f"{data_dir}/character/character.json", "r") as f:
            character_json = json.load(f)
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

            self.characters[char.id] = char
            self.characters_by_internal_name[char.internal_name] = char
            self.characters_by_name[char.name] = char
