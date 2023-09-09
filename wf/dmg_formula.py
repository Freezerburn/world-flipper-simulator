from __future__ import annotations
from typing import Self, Optional, TYPE_CHECKING, Tuple

from .enum import PowerFlip, Element

if TYPE_CHECKING:
    from .character import WorldFlipperCharacter
    from .game_state import GameState


BOW_FAR_LEFT = 0
BOW_NEAR_LEFT = 1
BOW_MIDDLE = 2
BOW_NEAR_RIGHT = 3
BOW_FAR_RIGHT = 4


class DamageFormulaContext:
    def __init__(self, char: Optional[WorldFlipperCharacter] = None, unison=None):
        self.valid = True
        self.char: Optional[WorldFlipperCharacter] = char
        self.unison = unison
        # Layout: Far Left, Near Left, Middle, Near Right, Far Right
        self.bow_pf_hits = [False, False, True, False, False]

        # These values aren't actually used for anything when calculating damage, but instead are here
        # to track things that are modified by abilities that we might want to see in the UI.
        self.combo = 0
        self.pf_combo_reduction = [0] * 3
        self.skill_charge = [0] * 3
        self.skill_charge_speed = [1] * 3
        self.skill_gauge_max = [100] * 3
        self.attack_buff_extension = 1
        self.pierce_buff_extension = 1
        self.pierce_active = False
        self.fever_gain_from_attacks = 1
        self.increased_hp = [1] * 6

        # The different types of methods of applying damage have their own bools to enable each of them.
        # Only a single of these should ever be applied at one time, because the game will only ever have
        # a single source of damage be created at a time.
        self.created_by_da = False
        self.created_by_pf_action = False
        self.created_by_skill_action = False
        self.created_by_ad = False

        self.weak = False
        self.target_has_pinch = False

        self.stat_mod_element_resists = {
            Element.FIRE: 1,
            Element.WATER: 1,
            Element.THUNDER: 1,
            Element.WIND: 1,
            Element.DARK: 1,
            Element.LIGHT: 1,
        }
        self.stat_mod_pf_resist_mult = 1
        self.stat_mod_da_resist_mult = 1
        self.stat_mod_sd_resist_mult = 1
        self.stat_mod_ad_resist_mult = 1

        # Is used as denominator in a division operation, so has to be non-zero.
        # NOTE: As far as I'm aware, there is nothing that increases the amount of direct attacks
        # in a single hit to ever exceed 2, so that cap will be hard-coded until such time as
        # something breaks that rule.
        self.stat_mod_additional_da_times = 1

        self.attack_modifier = 0
        self.total_resist = 0
        self.stat_mod_pinch_slayer = 0
        self.condition_slayer = 0
        self.character_slayer = 0
        self.stat_mod_adversity = 0
        self.attacker_fraction_health_lost = 0
        self.stat_mod_da_damage = 0
        self.stat_mod_additional_da_damage = 0
        self.stat_mod_pf_damage = 0
        self.stat_mod_pf_resist_multi = 0
        self.charge_level = 0
        self.stat_mod_pf_lv_damage_slayer_lv = 0
        self.stat_mod_pf_lv_damage_slayer = 0
        self.stat_mod_sd_damage = 0
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
        self.element_damage_cut = 0

    def combine(self, ctx: Self):
        # Always has a base of 1, so we need to combine only the potential difference from the base.
        self.stat_mod_pf_resist_mult += ctx.stat_mod_pf_resist_mult - 1
        self.stat_mod_ad_resist_mult += ctx.stat_mod_ad_resist_mult - 1
        self.stat_mod_sd_resist_mult += ctx.stat_mod_sd_resist_mult - 1
        self.stat_mod_ad_resist_mult += ctx.stat_mod_ad_resist_mult - 1

        self.attack_modifier += ctx.attack_modifier
        self.total_resist += ctx.total_resist
        self.stat_mod_pinch_slayer += ctx.stat_mod_pinch_slayer
        self.condition_slayer += ctx.condition_slayer
        self.character_slayer += ctx.character_slayer
        self.stat_mod_adversity += ctx.stat_mod_adversity
        self.attacker_fraction_health_lost += ctx.attacker_fraction_health_lost
        self.stat_mod_da_damage += ctx.stat_mod_da_damage
        self.stat_mod_additional_da_damage += ctx.stat_mod_additional_da_damage
        if self.stat_mod_additional_da_times == 1:
            self.stat_mod_additional_da_times = ctx.stat_mod_additional_da_times
        self.stat_mod_pf_damage += ctx.stat_mod_pf_damage
        if self.stat_mod_pf_lv_damage_slayer_lv == 0:
            self.stat_mod_pf_lv_damage_slayer_lv = ctx.stat_mod_pf_lv_damage_slayer_lv
        self.stat_mod_pf_lv_damage_slayer += ctx.stat_mod_pf_lv_damage_slayer
        self.stat_mod_sd_damage += ctx.stat_mod_sd_damage
        self.skill_multiplier += ctx.skill_multiplier
        self.skill_slayer += ctx.skill_slayer
        self.current_combos += ctx.current_combos
        self.total_coffin_counts += ctx.total_coffin_counts
        self.total_buff_counts += ctx.total_buff_counts
        if self.distance == 0:
            self.distance = ctx.distance
        self.stat_mod_ad_damage += ctx.stat_mod_ad_damage
        self.element_damage_cut += ctx.element_damage_cut

        if self.stat_mod_additional_da_times > 2:
            self.stat_mod_additional_da_times = 2

    def calculate(self, state: GameState) -> Tuple[float, float]:
        # Find the lowest possible random damage and the highest possible. Allows for displaying the full range
        # in a UI.
        low_range = self._calculate_internal(state, 0, -0.05)
        high_range = self._calculate_internal(state, 2, 0.05)
        return low_range, high_range

    def _calculate_internal(self, state: GameState, skill_rand, dmg_rand) -> float:
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
            raise RuntimeError(
                "Can only calculate damage if formula was given a character."
            )
        char_idx = state.party.index(self.char)

        # 1
        atk = self.char.attack(
            state.is_evolved(self.char), state.levels[char_idx], state.uncaps[char_idx]
        )
        # Main units inherit a quarter of a unison's attack, make sure to include that in the calculation.
        if self.unison is not None:
            unison_idx = state.party.index(self.unison)
            atk += (
                self.unison.attack(
                    state.is_evolved(self.unison),
                    state.levels[unison_idx],
                    state.uncaps[unison_idx],
                )
                * 0.25
            )
        dmg = atk * (1 + max(-0.5, self.attack_modifier))
        # 2
        if self.created_by_skill_action:
            # Random range: [0, 2]
            dmg += skill_rand + self.char.skill_base_dmg
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
            pf_mod_dmg = self._calc_pf_mod_dmg()
            if self.charge_level == 3:
                pf_mod_dmg *= 1 + self.stat_mod_pf_lv_damage_slayer
            dmg *= 1 + pf_mod_dmg
        # 14 - 19
        if self.created_by_skill_action:
            # 14, 15
            sdmg: float = (
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

    def _calc_pf_mod_dmg(self):
        match self.char.pf_type:
            case PowerFlip.SWORD:
                match self.charge_level:
                    case 0:
                        return 0
                    case 1:
                        return 2.75 * 3
                    case 2:
                        return 3.5 * 4
                    case 3:
                        return 5.5 * 5

            case PowerFlip.BOW:
                match self.charge_level:
                    case 0:
                        return 0
                    case 1:
                        if self.bow_pf_hits[BOW_MIDDLE]:
                            return 1.83 * 3
                        return 0
                    case 2:
                        total = 0
                        if self.bow_pf_hits[BOW_NEAR_LEFT]:
                            total += 0.5 * 2
                        if self.bow_pf_hits[BOW_MIDDLE]:
                            total += 2 * 4
                        if self.bow_pf_hits[BOW_NEAR_RIGHT]:
                            total += 0.5 * 2
                        return total
                    case 3:
                        total = 0
                        if self.bow_pf_hits[BOW_FAR_LEFT]:
                            total += 0.5 * 2
                        if self.bow_pf_hits[BOW_NEAR_LEFT]:
                            total += 1 * 3
                        if self.bow_pf_hits[BOW_MIDDLE]:
                            total += 2.5 * 4
                        if self.bow_pf_hits[BOW_NEAR_RIGHT]:
                            total += 1 * 3
                        if self.bow_pf_hits[BOW_FAR_RIGHT]:
                            total += 0.5 * 2
                        return total

            case PowerFlip.FIST:
                match self.charge_level:
                    case 0:
                        return 0
                    case 1:
                        return 2.8 + 0.9 * 3
                    case 2:
                        return 5.8 + 1.2 * 4
                    case 3:
                        return 12.5 + 1.5 * 5

            case PowerFlip.SPECIAL:
                match self.charge_level:
                    case 0:
                        return 0
                    case 1:
                        return 5
                    case 2:
                        return 7
                    case 3:
                        return 13

            case PowerFlip.SUPPORT:
                if self.charge_level == 3:
                    return 4
                return 0

    def changed_values(self):
        out = []
        for idx, sc in enumerate(self.skill_charge):
            if sc != 0:
                out.append((f"SKILL_CHARGE_{idx + 1}", sc))

        if self.stat_mod_pf_resist_mult != 1:
            out.append(("PF_RESIST", self.stat_mod_pf_resist_mult))
        if self.stat_mod_da_resist_mult != 1:
            out.append(("DA_RESIST", self.stat_mod_da_resist_mult))
        if self.stat_mod_sd_resist_mult != 1:
            out.append(("SD_RESIST", self.stat_mod_sd_resist_mult))
        if self.stat_mod_ad_resist_mult != 1:
            out.append(("AD_RESIST", self.stat_mod_ad_resist_mult))

        if self.attack_modifier > 0:
            out.append(("ATTACK_MODIFIER", self.attack_modifier))
        if self.total_resist > 0:
            out.append(("TOTAL_RESIST", self.total_resist))
        if self.stat_mod_pinch_slayer:
            out.append(("DOWNED_SLAYER", self.stat_mod_pinch_slayer))
        if self.condition_slayer > 0:
            out.append(("CONDITION_SLAYER", self.condition_slayer))
        if self.character_slayer > 0:
            out.append(("CHARACTER_SLAYER", self.character_slayer))
        if self.stat_mod_adversity > 0:
            # TODO
            pass
        if self.attacker_fraction_health_lost > 0:
            # TODO
            pass
        if self.stat_mod_da_damage > 0:
            out.append(("DA_DAMAGE", self.stat_mod_da_damage))
        if (
            self.stat_mod_additional_da_damage > 0
            and self.stat_mod_additional_da_times > 1
        ):
            # TODO: Multihit
            pass
        if self.stat_mod_pf_damage > 0:
            out.append(("PF_DAMAGE", self.stat_mod_pf_damage))
        if self.stat_mod_pf_resist_multi > 0:
            # TODO
            pass
        if self.charge_level > 0:
            out.append(("PF_LV", self.charge_level))
            out.append(("PF_MOD_DAMAGE", self._calc_pf_mod_dmg()))
        if self.stat_mod_pf_lv_damage_slayer > 0:
            out.append(("PF_LV_SLAYER", self.stat_mod_pf_lv_damage_slayer))
        if self.stat_mod_sd_damage > 0:
            out.append(("SD_DAMAGE", self.stat_mod_sd_damage))
        # TODO: Remaining attributes.
        return out

    def _fmt_resist(self, r, name):
        plus_minus = "+"
        if r < 1:
            plus_minus = "-"
        return f"  {plus_minus}{(r - 1) * 100}% {name} RESIST"

    def __str__(self):
        out = ["== WF DMG FORMULA START =="]
        if self.stat_mod_pf_resist_mult != 1:
            out.append(self._fmt_resist(self.stat_mod_pf_resist_mult, "PF"))
        if self.stat_mod_da_resist_mult != 1:
            out.append(self._fmt_resist(self.stat_mod_da_resist_mult, "DA"))
        if self.stat_mod_sd_resist_mult != 1:
            out.append(self._fmt_resist(self.stat_mod_sd_resist_mult, "SD"))
        if self.stat_mod_ad_resist_mult != 1:
            out.append(self._fmt_resist(self.stat_mod_ad_resist_mult, "AD"))

        if self.attack_modifier > 0:
            out.append(f"  +{self.attack_modifier * 100}% ATK")
        if self.total_resist > 0:
            out.append(f"  +{self.total_resist * 100}% TOTAL RESIST")
        if self.stat_mod_pinch_slayer:
            out.append(f"  +{self.stat_mod_pinch_slayer * 100}% DOWN DMG")
        if self.condition_slayer > 0:
            out.append(f"  +{self.condition_slayer * 100}% DMG TO DEBUFFED ENEMIES")
        if self.character_slayer:
            out.append(
                f"  +{self.character_slayer * 100}% DMG TO SPECIFIC ELEMENT/RACE"
            )
        if self.stat_mod_adversity > 0:
            # TODO
            pass
        if self.attacker_fraction_health_lost > 0:
            # TODO
            pass
        if self.stat_mod_da_damage > 0:
            out.append(f"  +{self.stat_mod_da_damage * 100}% DA DMG")
        if (
            self.stat_mod_additional_da_damage > 0
            and self.stat_mod_additional_da_times > 1
        ):
            # TODO: Multihit
            pass
        if self.stat_mod_pf_damage > 0:
            out.append(f"  +{self.stat_mod_pf_damage * 100}% PF DAMAGE")
        if self.stat_mod_pf_resist_multi > 0:
            # TODO
            pass
        if self.charge_level > 0:
            out.append(f"  Lv{self.charge_level} PF")
            out.append(f"  +{self._calc_pf_mod_dmg() * 100}% TOTAL DMG FOR PF LV")
        if self.stat_mod_pf_lv_damage_slayer > 0:
            out.append(f"  +{self.stat_mod_pf_lv_damage_slayer * 100}% DMG TO Lv3 PF")
        if self.stat_mod_sd_damage > 0:
            out.append(f"  +{self.stat_mod_sd_damage}% SD DMG")
        # TODO: Remaining attributes.
        out.append("== WF DAMAGE FORMULA END ==")
        return "\n".join(out)
