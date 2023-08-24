from abc import ABC, abstractmethod
from wfdata.wfeffect import Effect
from wfdata.wfdmgformula import DamageFormulaContext


class Character(ABC):
    def __init__(self):
        self.position = None
        self.a_lv = [0, 0, 0, 0, 0, 0]

        self.stars = 3
        self.level = 1
        self.uncaps = 0
        self.evolved = False
        self.base_atk = 100
        self.base_hp = 100
        self.element = None
        self.skill_base_cost = 0
        self.skill_evolve_cost = 0
        self.skill_multiplier = 0
        self.skill_base_damage = 0

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
