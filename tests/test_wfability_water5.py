from unittest import TestCase
import copy

from wf import WorldFlipperData, CharPosition, DamageFormulaContext, Element
from wf.wfenemy import Enemy
from wf.wfenum import Debuff
from wf.wfgamestate import GameState


class TestWorldFlipperAbilityWater5(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wf_data = WorldFlipperData("wf_data_json")

    def test_sonia_ab1(self):
        sonia, state = self._base_state("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(vagner, CharPosition.MAIN, 1)

        with self.subTest("ab1"):
            sub_state = copy.deepcopy(state)
            sub_state.combos_reached[30] = 3

            df = sonia.abilities[0][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.3, df.attack_modifier)
            df = sonia.abilities[0][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab2"):
            sub_state = copy.deepcopy(state)

            df = sonia.abilities[1][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(1.5, df.attack_buff_extension)
            df = sonia.abilities[1][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab3"):
            sub_state = copy.deepcopy(state)
            sub_state.buffs[0] = [1]

            df = sonia.abilities[2][0].eval_effect(sonia, sub_state)
            self.assertEqual(2, df.stat_mod_additional_da_times)
            self.assertAlmostEqual(0.5, df.stat_mod_additional_da_damage)
            df = sonia.abilities[2][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab4"):
            sub_state = copy.deepcopy(state)
            sub_state.skill_hits[0] = 23

            df = sonia.abilities[3][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(1.1, df.fever_gain_from_attacks)
            df = sonia.abilities[3][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

        with self.subTest("ab5"):
            sub_state = copy.deepcopy(state)
            sub_state.in_fever = True
            sub_state.ability_condition_active[0][4] = True

            df = sonia.abilities[4][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)
            df = sonia.abilities[4][0].eval_effect(vagner, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)

        with self.subTest("ab6"):
            sub_state = copy.deepcopy(state)
            sub_state.in_fever = True
            sub_state.ability_condition_active[0][5] = True

            df = sonia.abilities[5][0].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(0.4, df.attack_modifier)
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

    def test_acipher_ab1(self):
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
            self.assertAlmostEqual(0.4, df.stat_mod_da_damage)
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
            self.assertAlmostEqual(0.4, df.attack_modifier)
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
            self.assertAlmostEqual(0.2, df.attack_modifier)
            df = acipher.abilities[2][0].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

            df = acipher.abilities[2][1].eval_effect(acipher, sub_state)
            self.assertAlmostEqual(1.1, df.stat_mod_element_resists[Element.FIRE])
            df = acipher.abilities[2][1].eval_effect(sonia, sub_state)
            self.assertAlmostEqual(1.1, df.stat_mod_element_resists[Element.FIRE])
            df = acipher.abilities[2][1].eval_effect(vagner, sub_state)
            self.assertIsNone(df)

    def _base_state(self, char_name: str):
        state = GameState()
        char = self.wf_data.find(char_name)
        state.set_member(char, CharPosition.LEADER, level=80)
        state.ability_lvs[0][:] = [6] * 6
        state.enemy = Enemy()
        return char, state
