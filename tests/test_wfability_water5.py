from unittest import TestCase

from wf import WorldFlipperData, CharPosition, DamageFormulaContext
from wf.wfenemy import Enemy
from wf.wfgamestate import GameState


class TestWorldFlipperAbilityWater5(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wf_data = WorldFlipperData("wf_data_json")

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

    def _base_state(self, char_name: str):
        state = GameState()
        char = self.wf_data.find(char_name)
        state.set_member(char, CharPosition.LEADER, level=80)
        state.ability_lvs[0][:] = [6] * 6
        state.enemy = Enemy()
        return char, state
