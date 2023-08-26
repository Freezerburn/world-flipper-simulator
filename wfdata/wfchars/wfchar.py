from abc import ABC, abstractmethod
from wfdata.wfeffect import Effect
from wfdata.wfdmgformula import DamageFormulaContext


# TODO: Planning on deprecating this in favor of "WfJsonCharacter", which will likely get renamed.
class Character(ABC):
    def __init__(self, char_json):
        self.position = None
        self.a_lv = [0, 0, 0, 0, 0, 0]
        self.level = 1
        self.uncaps = 0
        self.evolved = False
        self.skill_multiplier = 0

        self.stars = char_json.stars
        self.races = char_json.races
        self.gender = char_json.gender
        self.base_atk = char_json.base_atk
        self.base_hp = char_json.base_hp
        self.element = char_json.element
        self.leader_skill_name = char_json.leader_skill_name
        self.skill_name = char_json.skill_name
        self.skill_name_evolve = char_json.skill_name_evolve
        self.skill_base_cost = char_json.skill_base_cost
        self.skill_evolve_cost = char_json.skill_evolve_cost
        self.skill_base_dmg = char_json.skill_base_dmg
        self.pf_type = char_json.pf_type

    def attack(self) -> float:
        evol_atk = 0
        if self.evolved:
            if self.stars == 1:
                evol_atk = 30
            elif self.stars == 2:
                evol_atk = 40
            elif self.stars == 3:
                evol_atk = 50
            elif self.stars == 4:
                evol_atk = 54
            else:
                evol_atk = 60

        return self._calc_stat(self.base_atk, evol_atk)

    def hp(self) -> float:
        evol_hp = 0
        if self.evolved:
            if self.stars == 1:
                evol_hp = 150
            elif self.stars == 2:
                evol_hp = 200
            elif self.stars == 3:
                evol_hp = 250
            elif self.stars == 4:
                evol_hp = 270
            else:
                evol_hp = 300

        return self._calc_stat(self.base_hp, evol_hp)

    def _calc_stat(self, base_stat, evol_stat):
        if 1 <= self.level <= 10:
            stat_mult = self.level / 10
        elif 11 <= self.level <= 80:
            stat_mult = 1 + (self.level - 10) / 14
        else:
            stat_mult = 6 + 3 * (self.level - 80) / 100

        if self.stars == 1:
            uncap_mult = 0.4
        elif self.stars == 2:
            uncap_mult = 0.5
        elif self.stars == 3:
            uncap_mult = 0.8
        elif self.stars == 4:
            uncap_mult = 1.5
        else:
            uncap_mult = 3.0

        return base_stat * stat_mult * (1 + self.uncaps * uncap_mult) + evol_stat

    @abstractmethod
    def image(self) -> str:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def leader_text(self) -> str:
        pass

    @abstractmethod
    def leader_effects(self) -> [Effect]:
        pass

    @abstractmethod
    def skill_text(self) -> str:
        pass

    @abstractmethod
    def skill_cost(self) -> float:
        pass

    @abstractmethod
    def skill_effects(self) -> [Effect]:
        pass

    @abstractmethod
    def ability_text(self) -> [str]:
        pass

    @abstractmethod
    def damage_contexts(self) -> [DamageFormulaContext]:
        pass
