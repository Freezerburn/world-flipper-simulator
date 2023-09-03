from unittest import TestCase
import copy

from wf import WorldFlipperData, CharPosition, DamageFormulaContext, Element, Buff
from wf.wfenemy import Enemy
from wf.wfenum import Debuff
from wf.wfgamestate import GameState


class TestWorldFlipperAbilityWater5(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wf_data = WorldFlipperData("wf_data_json")

    def test_sonia(self):
        sonia, state = self._base_state("brown_fighter")
        acipher = self.wf_data.find("ice_witch_2anv")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(acipher, CharPosition.UNISON, 0)
        state.set_member(vagner, CharPosition.MAIN, 1)

        with self.subTest("ab1"):
            sub_state = copy.deepcopy(state)
            sub_state.combos_reached[30] = 3

            df = sonia.abilities[0][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.3, df.attack_modifier)
            df = sonia.abilities[0][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = sonia.abilities[0][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab2"):
            sub_state = copy.deepcopy(state)

            df = sonia.abilities[1][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(1.5, df.attack_buff_extension)
            df = sonia.abilities[1][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = sonia.abilities[1][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab3"):
            sub_state = copy.deepcopy(state)
            sub_state.buffs[0] = [1]

            df = sonia.abilities[2][0].eval_effect(sonia, sub_state)
            self.assertEqual(2, df.stat_mod_additional_da_times)
            self.assertAlmostEqual(0.5, df.stat_mod_additional_da_damage)
            df = sonia.abilities[2][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = sonia.abilities[2][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab4"):
            sub_state = copy.deepcopy(state)
            sub_state.skill_hits[0] = 23

            df = sonia.abilities[3][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(1.1, df.fever_gain_from_attacks)
            df = sonia.abilities[3][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = sonia.abilities[3][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab5"):
            sub_state = copy.deepcopy(state)
            sub_state.in_fever = True
            sub_state.ability_condition_active[0][4] = True

            df = sonia.abilities[4][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)
            df = sonia.abilities[4][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = sonia.abilities[4][0].eval_effect(vagner, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)

        with self.subTest("ab6"):
            sub_state = copy.deepcopy(state)
            sub_state.in_fever = True
            sub_state.ability_condition_active[0][5] = True

            df = sonia.abilities[5][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)
            df = sonia.abilities[5][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = sonia.abilities[5][0].eval_effect(vagner, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)

    def test_suizen(self):
        suizen, state = self._base_state("onmyoji_boy")
        sonia = self.wf_data.find("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        acipher = self.wf_data.find("ice_witch_2anv")
        state.set_member(acipher, CharPosition.UNISON, 0)
        state.set_member(sonia, CharPosition.MAIN, 1)
        state.set_member(vagner, CharPosition.MAIN, 2)

        with self.subTest("ab1"):
            sub_state = copy.deepcopy(state)

            df = suizen.abilities[0][0].eval_effect(suizen, sub_state)
            self.assertAlmostEqual(1.2, df.increased_hp[0])
            df = suizen.abilities[0][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = suizen.abilities[0][0].eval_effect(sonia, sub_state)
            self.assertIsNone(df)
            df = suizen.abilities[0][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab2"):
            sub_state = copy.deepcopy(state)
            sub_state.enemy.debuffs = [Debuff.POISON]

            df = suizen.abilities[1][0].eval_effect(suizen, sub_state)
            self.assertAlmostEqual(0.5, df.attack_modifier)
            df = suizen.abilities[1][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = suizen.abilities[1][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.5, df.attack_modifier)
            df = suizen.abilities[1][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab3"):
            sub_state = copy.deepcopy(state)
            sub_state.enemy.debuffs = [Debuff.POISON]

            df = suizen.abilities[2][0].eval_effect(suizen, sub_state)
            self.assertAlmostEqual(0.25, df.condition_slayer)
            df = suizen.abilities[2][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = suizen.abilities[2][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.25, df.condition_slayer)
            df = suizen.abilities[2][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab4"):
            self.skipTest("[Suizen AB4] Damage from enemies not included in simulator.")

        with self.subTest("ab5"):
            sub_state = copy.deepcopy(state)
            sub_state.enemy.debuffs = [Debuff.POISON]

            df = suizen.abilities[4][0].eval_effect(suizen, sub_state)
            self.assertAlmostEqual(0.3, df.stat_mod_da_damage)
            df = suizen.abilities[4][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = suizen.abilities[4][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.3, df.stat_mod_da_damage)
            df = suizen.abilities[4][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab6"):
            sub_state = copy.deepcopy(state)
            sub_state.enemy.debuffs = [Debuff.POISON]

            df = suizen.abilities[5][0].eval_effect(suizen, sub_state)
            self.assertAlmostEqual(0.075, df.condition_slayer)
            df = suizen.abilities[5][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = suizen.abilities[5][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.075, df.condition_slayer)
            df = suizen.abilities[5][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

    def test_ellya(self):
        ellya, state = self._base_state("lightbullet_wiz_ny20")
        sonia = self.wf_data.find("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        acipher = self.wf_data.find("ice_witch_2anv")
        state.set_member(sonia, CharPosition.UNISON, 0)
        state.set_member(vagner, CharPosition.MAIN, 1)
        state.set_member(acipher, CharPosition.UNISON, 1)

        with self.subTest("leader"):
            # TODO: Implement leader abilities.
            pass

        with self.subTest("ab1"):
            sub_state = copy.deepcopy(state)
            sub_state.skill_activations[0] = 2
            sub_state.skill_activations[1] = 1

            df = ellya.abilities[0][0].eval_effect(ellya, sub_state)
            self.assertAlmostEqual(0.2, df.attack_modifier)
            df = ellya.abilities[0][0].eval_effect(sonia, sub_state)
            self.assertIsNone(df)
            df = ellya.abilities[0][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

            df = ellya.abilities[0][1].eval_effect(ellya, sub_state)
            self.assertAlmostEqual(0.2, df.skill_charge[0])
            df = ellya.abilities[0][1].eval_effect(sonia, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab2"):
            sub_state = copy.deepcopy(state)
            sub_state.combos_reached[30] = 2

            df = ellya.abilities[1][0].eval_effect(ellya, sub_state)
            self.assertAlmostEqual(0.25, df.attack_modifier)

        with self.subTest("ab3"):
            sub_state = copy.deepcopy(state)
            sub_state.skill_activations[0] = 1
            sub_state.skill_activations[1] = 2
            sub_state.skill_activations[2] = 1

            df = ellya.abilities[2][0].eval_effect(ellya, sub_state)
            self.assertAlmostEqual(0.6, df.stat_mod_sd_damage)
            df = ellya.abilities[2][1].eval_effect(ellya, sub_state)
            self.assertAlmostEqual(0.3, df.skill_charge[0])

        with self.subTest("ab4"):
            sub_state = copy.deepcopy(state)

            df = ellya.abilities[3][0].eval_effect(ellya, sub_state)
            self.assertAlmostEqual(0.5, df.skill_charge[0])

        with self.subTest("ab5"):
            sub_state = copy.deepcopy(state)
            sub_state.skill_activations[0] = 1
            sub_state.skill_activations[1] = 1
            sub_state.skill_activations[2] = 1

            df = ellya.abilities[4][0].eval_effect(ellya, sub_state)
            self.assertEqual(10, df.combo)
            df = ellya.abilities[4][1].eval_effect(ellya, sub_state)
            self.assertAlmostEqual(0.1, df.stat_mod_sd_damage)

        with self.subTest("ab6"):
            sub_state = copy.deepcopy(state)
            sub_state.skill_activations[0] = 1
            sub_state.skill_activations[1] = 1
            sub_state.skill_activations[2] = 1

            df = ellya.abilities[5][0].eval_effect(ellya, sub_state)
            self.assertAlmostEqual(0.15, df.stat_mod_sd_damage)

    def test_cipher(self):
        cipher, state = self._base_state("ice_witch")
        sonia = self.wf_data.find("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        acipher = self.wf_data.find("ice_witch_2anv")
        state.set_member(sonia, CharPosition.UNISON, 0, level=100)
        state.set_member(vagner, CharPosition.MAIN, 1, level=100)
        state.set_member(acipher, CharPosition.MAIN, 2, level=100)

        with self.subTest("leader"):
            pass

        with self.subTest("ab1"):
            sub_state = copy.deepcopy(state)
            df = cipher.abilities[0][0].eval_effect(cipher, sub_state)
            self.assertIsNone(df)

            sub_state.enemy.debuffs = [Debuff.SLOW]
            df = cipher.abilities[0][0].eval_effect(cipher, sub_state)
            self.assertAlmostEqual(0.1, df.condition_slayer)
            df = cipher.abilities[0][0].eval_effect(vagner, sub_state)
            self.assertAlmostEqual(0.1, df.condition_slayer)

        with self.subTest("ab2"):
            sub_state = copy.deepcopy(state)

            df = cipher.abilities[1][0].eval_effect(cipher, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)
            df = cipher.abilities[1][0].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)
            df = cipher.abilities[1][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

            sub_state.current_hp[0] = sub_state.max_hp[0] * 0.8
            df = cipher.abilities[1][0].eval_effect(cipher, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)

            sub_state.current_hp[0] = 50
            df = cipher.abilities[1][0].eval_effect(cipher, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab3"):
            sub_state = copy.deepcopy(state)

            df = cipher.abilities[2][0].eval_effect(cipher, sub_state)
            self.assertAlmostEqual(1.3, df.stat_mod_element_resists[Element.FIRE])
            df = cipher.abilities[2][1].eval_effect(cipher, sub_state)
            self.assertAlmostEqual(0.6, df.attack_modifier)
            df = cipher.abilities[2][0].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(1.3, df.stat_mod_element_resists[Element.FIRE])
            df = cipher.abilities[2][1].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(0.6, df.attack_modifier)

            sub_state.current_hp[2] = 50
            df = cipher.abilities[2][0].eval_effect(cipher, sub_state)
            self.assertAlmostEqual(1.3, df.stat_mod_element_resists[Element.FIRE])
            df = cipher.abilities[2][1].eval_effect(cipher, sub_state)
            self.assertAlmostEqual(0.6, df.attack_modifier)
            df = cipher.abilities[2][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)
            df = cipher.abilities[2][1].eval_effect(acipher, sub_state)
            self.assertIsNone(df)

            sub_state.current_hp[0] = 50
            sub_state.current_hp[2] = sub_state.max_hp[2]
            df = cipher.abilities[2][0].eval_effect(cipher, sub_state)
            self.assertIsNone(df)
            df = cipher.abilities[2][1].eval_effect(cipher, sub_state)
            self.assertIsNone(df)
            df = cipher.abilities[2][0].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(1.3, df.stat_mod_element_resists[Element.FIRE])
            df = cipher.abilities[2][1].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(0.6, df.attack_modifier)

        with self.subTest("ab4"):
            sub_state = copy.deepcopy(state)

        with self.subTest("ab5"):
            sub_state = copy.deepcopy(state)

        with self.subTest("ab6"):
            sub_state = copy.deepcopy(state)

    def test_selene(self):
        selene, state = self._base_state("commander")
        sonia = self.wf_data.find("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        acipher = self.wf_data.find("ice_witch_2anv")
        state.set_member(sonia, CharPosition.UNISON, 0, level=100)
        state.set_member(vagner, CharPosition.MAIN, 1, level=100)
        state.set_member(acipher, CharPosition.UNISON, 1, level=100)

        with self.subTest("ab1"):
            sub_state = copy.deepcopy(state)

            df = selene.abilities[0][0].eval_effect(selene, sub_state)
            self.assertAlmostEqual(0.2, df.attack_modifier)
            df = selene.abilities[0][1].eval_effect(selene, sub_state)
            self.assertAlmostEqual(1.15, df.attack_buff_extension)

            df = selene.abilities[0][0].eval_effect(sonia, sub_state)
            self.assertIsNone(df)
            df = selene.abilities[0][1].eval_effect(sonia, sub_state)
            self.assertIsNone(df)

            df = selene.abilities[0][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)
            df = selene.abilities[0][1].eval_effect(vagner, sub_state)
            self.assertAlmostEqual(1.15, df.attack_buff_extension)

        with self.subTest("ab2"):
            sub_state = copy.deepcopy(state)
            sub_state.buffs[0] = [Buff.ATTACK]

            df = selene.abilities[1][0].eval_effect(selene, sub_state)
            self.assertAlmostEqual(0.2, df.attack_modifier)
            df = selene.abilities[1][1].eval_effect(selene, sub_state)
            self.assertAlmostEqual(0.2, df.stat_mod_da_damage)

            df = selene.abilities[1][0].eval_effect(vagner, sub_state)
            self.assertAlmostEqual(0.2, df.attack_modifier)
            df = selene.abilities[1][1].eval_effect(vagner, sub_state)
            self.assertAlmostEqual(0.2, df.stat_mod_da_damage)

            sub_state.buffs[0] = []
            df = selene.abilities[1][0].eval_effect(selene, sub_state)
            self.assertIsNone(df)
            df = selene.abilities[1][1].eval_effect(selene, sub_state)
            self.assertIsNone(df)
            df = selene.abilities[1][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)
            df = selene.abilities[1][1].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab3"):
            sub_state = copy.deepcopy(state)

            df = selene.abilities[2][0].eval_effect(selene, sub_state)
            self.assertAlmostEqual(0.7, df.stat_mod_da_damage)
            df = selene.abilities[2][1].eval_effect(selene, sub_state)
            self.assertAlmostEqual(1.5, df.stat_mod_da_damage)
            df = selene.abilities[2][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)
            df = selene.abilities[2][1].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

            sub_state.current_hp[0] = sub_state.max_hp[0] * 0.75
            df = selene.abilities[2][0].eval_effect(selene, sub_state)
            self.assertAlmostEqual(0.7, df.stat_mod_da_damage)
            df = selene.abilities[2][1].eval_effect(selene, sub_state)
            self.assertIsNone(df)

            sub_state.current_hp[0] = 50
            df = selene.abilities[2][0].eval_effect(selene, sub_state)
            self.assertIsNone(df)
            df = selene.abilities[2][1].eval_effect(selene, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab4"):
            sub_state = copy.deepcopy(state)
            df = selene.abilities[3][0].eval_effect(selene, sub_state)
            self.assertAlmostEqual(0.5, df.skill_charge[0])

        with self.subTest("ab5"):
            sub_state = copy.deepcopy(state)
            sub_state.ability_condition_active[0][4] = True
            df = selene.abilities[4][0].eval_effect(selene, sub_state)
            self.assertAlmostEqual(0.6, df.attack_modifier)

            sub_state.set_member(selene, CharPosition.UNISON, 1, level=100)
            sub_state.ability_lvs[4][4] = 6
            sub_state.ability_condition_active[4][4] = True
            df = selene.abilities[4][0].eval_effect(selene, sub_state)
            self.assertAlmostEqual(0.6, df.attack_modifier)

        with self.subTest("ab6"):
            sub_state = copy.deepcopy(state)
            sub_state.buffs[0] = [Buff.ATTACK, Buff.ATTACK]

            df = selene.abilities[5][0].eval_effect(selene, sub_state)
            self.assertAlmostEqual(0.1, df.attack_modifier)
            df = selene.abilities[5][0].eval_effect(vagner, sub_state)
            self.assertAlmostEqual(0.1, df.attack_modifier)

    def test_acipher(self):
        acipher, state = self._base_state("ice_witch_2anv")
        sonia = self.wf_data.find("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(sonia, CharPosition.UNISON, 0)
        state.set_member(vagner, CharPosition.MAIN, 1)

        with self.subTest("ab1"):
            sub_state = copy.deepcopy(state)
            sub_state.enemy.debuffs = [1, 2]

            df = acipher.abilities[0][0].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(0.4, df.stat_mod_da_damage)
            df = acipher.abilities[0][0].eval_effect(sonia, sub_state)
            self.assertIsNone(df)
            df = acipher.abilities[0][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

            sub_state.set_member(sonia, CharPosition.LEADER)
            sub_state.set_member(acipher, CharPosition.UNISON, 0)
            sub_state.ability_lvs[1][0] = 6
            df = acipher.abilities[0][0].eval_effect(sonia, sub_state)
            self.assertIsNone(df)
            df = acipher.abilities[0][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab2"):
            sub_state = copy.deepcopy(state)
            sub_state.enemy.debuffs = [1, 2]

            df = acipher.abilities[1][0].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)
            df = acipher.abilities[1][0].eval_effect(sonia, sub_state)
            self.assertIsNone(df)
            df = acipher.abilities[1][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

            sub_state.set_member(sonia, CharPosition.LEADER)
            sub_state.set_member(acipher, CharPosition.UNISON, 0)
            sub_state.ability_lvs[1][1] = 6
            df = acipher.abilities[1][0].eval_effect(sonia, sub_state)
            self.assertIsNone(df)
            df = acipher.abilities[1][0].eval_effect(acipher, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab3"):
            sub_state = copy.deepcopy(state)
            sub_state.enemy.debuffs = [1, 2]

            df = acipher.abilities[2][0].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(0.2, df.attack_modifier)
            df = acipher.abilities[2][0].eval_effect(sonia, sub_state)
            self.assertIsNone(df)
            df = acipher.abilities[2][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

            df = acipher.abilities[2][1].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(1.1, df.stat_mod_element_resists[Element.FIRE])
            df = acipher.abilities[2][1].eval_effect(sonia, sub_state)
            self.assertIsNone(df)
            df = acipher.abilities[2][1].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

    def _base_state(self, char_name: str):
        state = GameState()
        char = self.wf_data.find(char_name)
        state.set_member(char, CharPosition.LEADER, level=80)
        state.ability_lvs[0][:] = [6] * 6
        state.enemy = Enemy()
        return char, state
