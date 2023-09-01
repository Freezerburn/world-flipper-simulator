from unittest import TestCase

from wf import WorldFlipperData, CharPosition, DamageFormulaContext, Element
from wf.wfenemy import Enemy
from wf.wfgamestate import GameState


class TestWorldFlipperAbilityWater5(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wf_data = WorldFlipperData("wf_data_json")

    def test_sonia_ab1(self):
        sonia, state = self._base_state("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(vagner, CharPosition.UNISON, 0)
        state.combos_reached[30] = 3

        df = sonia.abilities[0][0].eval_effect(sonia, state)
        self.assertAlmostEqual(0.3, df.attack_modifier)
        df = sonia.abilities[0][0].eval_effect(vagner, state)
        self.assertIsNone(df)

    def test_sonia_ab2(self):
        sonia, state = self._base_state("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(vagner, CharPosition.MAIN, 1)

        df = sonia.abilities[1][0].eval_effect(sonia, state)
        self.assertAlmostEqual(1.5, df.attack_buff_extension)
        df = sonia.abilities[1][0].eval_effect(vagner, state)
        self.assertIsNone(df)

    def test_sonia_ab3(self):
        sonia, state = self._base_state("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(vagner, CharPosition.MAIN, 1)
        state.buffs[0] = [1]

        df = sonia.abilities[2][0].eval_effect(sonia, state)
        self.assertEqual(2, df.stat_mod_additional_da_times)
        self.assertAlmostEqual(0.5, df.stat_mod_additional_da_damage)
        df = sonia.abilities[2][0].eval_effect(vagner, state)
        self.assertIsNone(df)

    def test_sonia_ab4(self):
        sonia, state = self._base_state("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(vagner, CharPosition.MAIN, 1)
        state.skill_hits[0] = 23

        df = sonia.abilities[3][0].eval_effect(sonia, state)
        self.assertAlmostEqual(1.1, df.fever_gain_from_attacks)
        df = sonia.abilities[3][0].eval_effect(vagner, state)
        self.assertIsNone(df)

    def test_sonia_ab5(self):
        sonia, state = self._base_state("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(vagner, CharPosition.MAIN, 1)
        state.in_fever = True
        state.ability_condition_active[0][4] = True

        df = sonia.abilities[4][0].eval_effect(sonia, state)
        self.assertAlmostEqual(0.4, df.attack_modifier)
        df = sonia.abilities[4][0].eval_effect(vagner, state)
        self.assertAlmostEqual(0.4, df.attack_modifier)

    def test_sonia_ab6(self):
        sonia, state = self._base_state("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(vagner, CharPosition.MAIN, 1)
        state.in_fever = True
        state.ability_condition_active[0][5] = True

        df = sonia.abilities[5][0].eval_effect(sonia, state)
        self.assertAlmostEqual(0.4, df.attack_modifier)
        df = sonia.abilities[5][0].eval_effect(vagner, state)
        self.assertAlmostEqual(0.4, df.attack_modifier)

    def test_acipher_ab1(self):
        acipher, state = self._base_state("ice_witch_2anv")
        sonia = self.wf_data.find("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(sonia, CharPosition.UNISON, 0)
        state.set_member(vagner, CharPosition.MAIN, 1)
        state.enemy.debuffs = [1, 2]

        df = acipher.abilities[0][0].eval_effect(acipher, state)
        self.assertAlmostEqual(0.4, df.stat_mod_da_damage)
        df = acipher.abilities[0][0].eval_effect(sonia, state)
        self.assertAlmostEqual(0.4, df.stat_mod_da_damage)
        df = acipher.abilities[0][0].eval_effect(vagner, state)
        self.assertIsNone(df)

        state.set_member(sonia, CharPosition.LEADER)
        state.set_member(acipher, CharPosition.UNISON, 0)
        state.ability_lvs[1][0] = 6
        df = acipher.abilities[0][0].eval_effect(sonia, state)
        self.assertIsNone(df)
        df = acipher.abilities[0][0].eval_effect(acipher, state)
        self.assertIsNone(df)

    def test_acipher_ab2(self):
        acipher, state = self._base_state("ice_witch_2anv")
        sonia = self.wf_data.find("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(sonia, CharPosition.UNISON, 0)
        state.set_member(vagner, CharPosition.MAIN, 1)
        state.enemy.debuffs = [1, 2]

        df = acipher.abilities[1][0].eval_effect(acipher, state)
        self.assertAlmostEqual(0.4, df.attack_modifier)
        df = acipher.abilities[1][0].eval_effect(sonia, state)
        self.assertAlmostEqual(0.4, df.attack_modifier)
        df = acipher.abilities[1][0].eval_effect(vagner, state)
        self.assertIsNone(df)

        state.set_member(sonia, CharPosition.LEADER)
        state.set_member(acipher, CharPosition.UNISON, 0)
        state.ability_lvs[1][1] = 6
        df = acipher.abilities[1][0].eval_effect(sonia, state)
        self.assertIsNone(df)
        df = acipher.abilities[1][0].eval_effect(acipher, state)
        self.assertIsNone(df)

    def test_acipher_ab3(self):
        acipher, state = self._base_state("ice_witch_2anv")
        sonia = self.wf_data.find("brown_fighter")
        vagner = self.wf_data.find("fire_dragon")
        state.set_member(sonia, CharPosition.UNISON, 0)
        state.set_member(vagner, CharPosition.MAIN, 1)
        state.enemy.debuffs = [1, 2]

        df = acipher.abilities[2][0].eval_effect(acipher, state)
        self.assertAlmostEqual(0.2, df.attack_modifier)
        df = acipher.abilities[2][0].eval_effect(sonia, state)
        self.assertAlmostEqual(0.2, df.attack_modifier)
        df = acipher.abilities[2][0].eval_effect(vagner, state)
        self.assertIsNone(df)

        df = acipher.abilities[2][1].eval_effect(acipher, state)
        self.assertAlmostEqual(1.1, df.stat_mod_element_resists[Element.FIRE])
        df = acipher.abilities[2][1].eval_effect(sonia, state)
        self.assertAlmostEqual(1.1, df.stat_mod_element_resists[Element.FIRE])
        df = acipher.abilities[2][1].eval_effect(vagner, state)
        self.assertIsNone(df)

    def _base_state(self, char_name: str):
        state = GameState()
        char = self.wf_data.find(char_name)
        state.set_member(char, CharPosition.LEADER, level=80)
        state.ability_lvs[0][:] = [6] * 6
        state.enemy = Enemy()
        return char, state
