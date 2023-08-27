from .wfability import WorldFlipperAbility
from .wfenum import PowerFlip, Element


class WorldFlipperCharacter:
    def __init__(self, key, data):
        self.id = key
        self.position = None

        data_arr = data[0]
        self.internal_name = data_arr[0]
        self.races = data_arr[4].split(",")
        self.gender = data_arr[7]
        self.leader_skill_name = data_arr[10]
        self.stars = int(data_arr[2])
        self.ability_ids = data_arr[11:16]
        self.abilities: list[list[WorldFlipperAbility]] = []

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
