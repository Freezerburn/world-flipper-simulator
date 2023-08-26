from __future__ import annotations


class DamageFormulaContext:
    def __init__(self, char=None, enemy=None, unison=None):
        self.char = char
        self.enemy = enemy
        self.unison = unison

        self.element = None
        self.target_character = None
        self.requires_main = False
        self.pf_action_type = None

        # The different types of methods of applying damage have their own bools to enable each of them.
        # Only a single of these should ever be applied at one time, because the game will only ever have
        # a single source of damage be created at a time.
        self.created_by_da = False
        self.created_by_pf_action = False
        self.created_by_skill_action = False
        self.created_by_ad = False

        self.attack_modifier = 0
        self.created_by_skill_action = 0
        self.skill_base_damage = 0
        self.weak = False
        self.total_resist = 0
        self.target_has_pinch = False
        self.stat_mod_pinch_slayer = 0
        self.condition_slayer = 0
        self.character_slayer = 0
        self.stat_mod_adversity = 0
        self.attacker_fraction_health_lost = 0
        self.stat_mod_da_damage = 0
        self.stat_mod_da_resist_mult = 0
        self.stat_mod_additional_da_damage = 0
        self.stat_mod_additional_da_times = 0
        self.stat_mod_pf_damage = 0
        self.stat_mod_pf_resist_multi = 0
        self.stat_mod_pf_resist_mult = 0
        self.charge_level = 0
        self.stat_mod_pf_lv_damage = 0
        self.stat_mod_pf_lv_damage_slayer_lv = 0
        self.stat_mod_pf_lv_damage_slayer = 0
        self.stat_mod_sd_damage = 0
        self.stat_mod_sd_resist_mult = 0
        self.skill_multiplier = 0
        self.skill_slayer = 0
        self.enables_combo_bonus = False
        self.current_combos = 0
        self.enables_coffin_count_bonus = False
        self.total_coffin_counts = 0
        self.enables_buff_count_bonus = False
        self.total_buff_counts = 0
        self.enables_range_bonus = False
        self.distance = 0
        self.stat_mod_ad_damage = 0
        self.stat_mod_ad_resist_mult = 0
        self.element_damage_cut = 0

    def apply(self, ctx: DamageFormulaContext, char):
        # Because certain abilities are marked as "own <thing>", we need a way to prevent those buffs from applying
        # to any character that is not the target of "own". So those characters can mark a target when creating the
        # context, and if it doesn't match the given character, that context is ignored.
        if ctx.target_character is not None and ctx.target_character != char.name():
            return
        # If the given context has an element restriction, only apply it if it matches the character's element.
        if ctx.element is not None and ctx.element != char.element:
            return

    def calculate(self) -> (float, float):
        # Find the lowest possible random damage and the highest possible. Allows for displaying the full range
        # in a UI.
        low_range = self._calculate_internal(0, -0.05)
        high_range = self._calculate_internal(2, 0.05)
        return low_range, high_range

    def _calculate_internal(self, skill_rand, dmg_rand) -> float:
        """
        1 unitAttack * (1 + max ( -0.5 , attackModifier ) )
        2 + createdBySkillAction ? ( randomInt (0 , 2) + skillBaseDamage )
        3 * WeakAndHostile ? 1.5 : NotWeakAndNotHostile ? 0.5
        4 * totalResist > 0 ? 1/(1 + totalResist ) : (1 - totalResist )
        5 * targetHasPinch ? 1.5 * (1 + statModPinchSlayer )
        6 * targetHasGuard ? 0.2
        7 * (1 + conditionSlayer )
        8 * (1 + characterSlayer )
        9 * (1 + statModAdversity * attackerFractionHealthLost )
        10 * createdByDA ? (1 + statModDADamage ) * statModDAResistMult
        11   * (1 + statModAdditionalDADamage ) / statModAdditionalDATimes
        12 * createdByPFAction ? (1 + statModPFDamage ) * statModPFResistMult
        13 * createdByPFAction AND ChargeLevel > 0 ? (1 + statModPFLvDamage * (1 +
             statModPFLvDamageSlayer ) )
        14 * createdBySkillAction ? (1 + statModSDamage ) * statModSDResistMult
        15   * skillMultiplier * (1 + skillSlayer )
        16   * enablesComboBonus ? (1 + 0.005 * CurrentCombos )
        17   * enablesCoffinCountBonus ? (1 + 0.026 * TotalCoffinCounts )
        18   * enablesBuffCountBonus ? (1 + 0.1 * TotalBuffCounts )
        19   * enablesRangeBonus ? (1 + min (0.5 , Distance ^2/700) )
        20 * createdByAD ? (1 + statModADDamage ) * statModADResistMult
        21 * (1 + randomFloat ( -0.05 , 0.05) )
        22 - elementDamageCut
        23 * targetIsInvincible ? 0
        """
        # All lines of Python are preceded by a comment with a number. That number corresponds to the same line in
        # the above formula.
        if self.char is None:
            raise RuntimeError("Can only calculate damage if formula was given a character.")

        # 1
        atk = self.char.attack()
        # Main units inherit a quarter of a unison's attack, make sure to include that in the calculation.
        if self.unison is not None:
            atk += self.unison.attack() * 0.25
        dmg = atk * (1 + max(-0.5, self.attack_modifier))
        # 2
        if self.created_by_skill_action:
            # Random range: [0, 2]
            dmg += skill_rand + self.skill_base_damage
        # 3
        if self.weak:
            dmg *= 1.5
        # 4
        if self.total_resist > 0:
            dmg *= 1 / (1 + self.total_resist)
        else:
            dmg *= 1 - self.total_resist
        # 5
        if self.target_has_pinch:
            dmg *= 1.5 * (1 + self.stat_mod_pinch_slayer)
        # 6: Ignore this line, only calculate damage against enemies.
        # 7
        dmg *= 1 + self.condition_slayer
        # 8
        dmg *= 1 + self.character_slayer
        # 9
        dmg *= 1 + self.stat_mod_adversity * self.attacker_fraction_health_lost
        # 10, 11
        if self.created_by_da:
            dmg *= (
                (1 + self.stat_mod_da_damage)
                * self.stat_mod_da_resist_mult
                * (1 + self.stat_mod_additional_da_damage)
                / self.stat_mod_additional_da_times
            )
        # 12
        if self.created_by_pf_action:
            dmg *= (1 + self.stat_mod_pf_damage) * self.stat_mod_pf_resist_mult
        # 13
        if self.created_by_pf_action and self.charge_level > 0:
            dmg *= 1 + self.stat_mod_pf_lv_damage * (1 + self.stat_mod_pf_lv_damage_slayer)
        # 14 - 19
        if self.created_by_skill_action:
            # 14, 15
            sdmg = (
                (1 + self.stat_mod_sd_damage)
                * self.stat_mod_sd_resist_mult
                * self.skill_multiplier
                * (1 + self.skill_slayer)
            )
            # 16
            if self.enables_combo_bonus:
                sdmg *= 1 + 0.005 * self.current_combos
            # 17
            if self.enables_coffin_count_bonus:
                sdmg *= 1 + 0.026 * self.total_coffin_counts
            # 18
            if self.enables_buff_count_bonus:
                sdmg *= 1 + 0.1 * self.total_buff_counts
            # 19
            if self.enables_range_bonus:
                sdmg *= 1 + min(0.5, self.distance * self.distance / 700)
            dmg *= sdmg
        # 20
        if self.created_by_ad:
            dmg *= (1 + self.stat_mod_ad_damage) * self.stat_mod_ad_resist_mult
        # 21
        # Random range: [-0.05, 0.05]
        dmg *= 1 + dmg_rand
        # 22
        dmg -= self.element_damage_cut
        # 23: Ignore this line: We don't care about invincibility state.
        return dmg
