from abc import ABC

from wf.wfeffects.wfeffect import WorldFlipperCondition
from wf.wfenum import element_ab_to_enum


class WorldFlipperContinuousCondition(WorldFlipperCondition, ABC):
    def _calc_abil_lv(self) -> int:
        v_min = int(self.ability.continuous_condition_min) / 100_000
        v_max = int(self.ability.continuous_condition_max) / 100_000
        step = abs(v_max - v_min) / 5
        return v_min + step * (self.lv - 1)


class MultiballCountContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_multiball"]

    def eval(self) -> bool:
        return self.state.num_multiballs > self._calc_abil_lv()


class BuffActiveContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_condition"]

    def eval(self) -> bool:
        return len(self.state.buffs[self.state.main_index(self.target_char_idx)]) > 0


class SkillGaugeAboveContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return ["ability_description_during_trigger_kind_skill_gauge_high"]

    def eval(self) -> bool:
        amt = self._calc_abil_lv()
        match self.ability.continuous_effect_target:
            case "0":
                target_char_idx = self.ability_char_idx
            case "7":
                target_char_idx = self.target_char_idx
            case _:
                raise RuntimeError(
                    f"[{self.ui_name[0]}] Unhandled continuous "
                    f"target: {self.ability.continuous_effect_target}"
                )
        if self.state.skill_charge[target_char_idx] <= amt:
            return False
        return True


class DebuffsOnEnemyContinuousCondition(WorldFlipperContinuousCondition):
    @staticmethod
    def ui_key() -> list[str]:
        return [
            "ability_description_during_trigger_kind_one_of_enemy_condition_high_count"
        ]

    def eval(self) -> bool:
        enemy = self.state.enemy
        if enemy is None:
            return False
        element = element_ab_to_enum(self.ability.continuous_effect_element)
        if element is not None and self.target_char.element != element:
            return False

        self.multiplier = len(enemy.debuffs) * self._calc_abil_lv()
        return True
