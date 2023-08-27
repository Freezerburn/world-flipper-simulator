import json
import weakref

from .wfchar import WorldFlipperCharacter
from .wfability import WorldFlipperAbility


class WorldFlipperData:
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
            char = WorldFlipperCharacter(key, character_json[key])
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
                    # Use a weakref of the character to prevent a cycle. Should always be safe because
                    # once a character is no longer being referenced we should also no longer be able to
                    # access/use the ability.
                    effects.append(
                        WorldFlipperAbility(ability_effect_json, weakref.proxy(char))
                    )
                char.abilities.append(effects)

            self.characters[char.id] = char
            self.characters_by_internal_name[char.internal_name] = char
            self.characters_by_name[char.name] = char

    def find(self, key: str):
        if key in self.characters:
            return self.characters[key]
        elif key in self.characters_by_internal_name:
            return self.characters_by_internal_name[key]
        elif key in self.characters_by_name:
            return self.characters_by_name[key]

        if key[-1].isdigit():
            if key[-2] == "_":
                key = key[:-2]
            else:
                key = key[:-1]
            return self.find(key)

        raise IndexError(f"No character with key {key} in database.")
