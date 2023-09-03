from abc import ABC

from wf.wfeffects.wfeffect import WorldFlipperCondition
from wf.wfenum import element_ab_to_enum, Buff


class WorldFlipperContinuousCondition(WorldFlipperCondition, ABC):
    pass


class HPAbovePercentContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_hp_high"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in char_idxs:
            current_hp = self.state.current_hp[self.state.mains_only_index(idx)]
            max_hp = self.state.max_hp[self.state.mains_only_index(idx)]
            if (current_hp / max_hp) < self._calc_abil_lv():
                return False
        return True


class MultiballCountContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_multiball"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        return self.state.num_multiballs > self._calc_abil_lv()


class BuffActiveContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_condition"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in char_idxs:
            if len(self.state.buffs[self.state.main_index(idx)]) == 0:
                return False
        return True


class AttackBuffActiveContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_condition"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        for idx in self._only_mains(char_idxs):
            try:
                self.state.buffs[idx].index(Buff.ATTACK)
            except ValueError:
                return False
        return True


class SkillGaugeAboveContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_skill_gauge_high"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        amt = self._calc_abil_lv()
        for idx in char_idxs:
            if self.state.skill_charge[self.state.main_index(idx)] <= amt:
                return False
        return True


class DebuffsOnEnemyContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return [
            "ability_description_during_trigger_kind_one_of_enemy_condition_high_count"
        ]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        enemy = self.state.enemy
        if enemy is None:
            return False
        self.multiplier = len(enemy.debuffs) * self._calc_abil_lv()
        return True


class AttackBuffsOnSelfContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_condition_high_count"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        self.multiplier = 0
        for idx in self._only_mains(char_idxs):
            self.multiplier += (
                self.state.buffs[idx].count(Buff.ATTACK) * self._calc_abil_lv()
            )
        if self.multiplier == 0:
            return False
        return True


class PierceActiveContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_condition"]

    def _apply_effect(self, char_idxs: list[int]) -> bool:
        return self.state.pierce_active
