from unittest import TestCase

from wf import WorldFlipperData, CharPosition, DamageFormulaContext
from wf.wfenemy import Enemy
from wf.wfgamestate import GameState


class TestWorldFlipperAbilityFire5(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wf_data = WorldFlipperData("wf_data_json")

    def test_vagner_ab1(self):
        """
        Verifies that Vagner's ability 1, which increases powerflip damage, correctly applies
        to only the leader.
        """
        vagner, state = self._base_state("fire_dragon")
        df = vagner.abilities[0][0].eval_effect(vagner, state)
        self.assertAlmostEqual(0.3, df.stat_mod_pf_damage)

        ahanabi = self.wf_data.find("kunoichi_1anv")
        state.set_member(ahanabi, CharPosition.LEADER)
        state.set_member(vagner, CharPosition.UNISON, 0)
        state.ability_lvs[1][0] = 6

        df = vagner.abilities[0][0].eval_effect(ahanabi, state)
        self.assertAlmostEqual(0.3, df.stat_mod_pf_damage)
        df = vagner.abilities[0][0].eval_effect(vagner, state)
        self.assertIsNone(df)

    def test_vagner_ab2(self):
        """
        Checks that Vagner's ability 2, increasing attack after a number of powerflips, correctly
        applies to only him.
        """
        vagner, state = self._base_state("fire_dragon")
        ahanabi = self.wf_data.find("kunoichi_1anv")
        state.set_member(ahanabi, CharPosition.UNISON, 0)
        state.set_powerflips(1, 11)

        df = vagner.abilities[1][0].eval_effect(vagner, state)
        self.assertAlmostEqual(0.3, df.attack_modifier)
        df = vagner.abilities[1][0].eval_effect(ahanabi, state)
        self.assertIsNone(df)

    def test_vagner_ab3(self):
        vagner, state = self._base_state("fire_dragon")
        ahanabi = self.wf_data.find("kunoichi_1anv")
        df = vagner.abilities[2][0].eval_effect(vagner, state)
        self.assertEqual(5, df.pf_combo_reduction[2])
        df = vagner.abilities[2][1].eval_effect(vagner, state)
        self.assertAlmostEqual(0.4, df.stat_mod_pf_damage)

        state.set_member(ahanabi, CharPosition.LEADER)
        state.set_member(vagner, CharPosition.UNISON, 0)
        state.ability_lvs[1][3] = 6

        df = vagner.abilities[2][1].eval_effect(ahanabi, state)
        self.assertIsNone(df)
        df = vagner.abilities[2][1].eval_effect(vagner, state)
        self.assertIsNone(df)

    def test_vagner_ab4(self):
        vagner, state = self._base_state("fire_dragon")
        df = vagner.abilities[3][0].eval_effect(vagner, state)
        self.assertAlmostEqual(0.5, df.skill_charge[0])
        self.assertEqual(0, len(df.changed_values()))

    def test_vagner_ab5(self):
        vagner, state = self._base_state("fire_dragon")
        df = vagner.abilities[4][1].eval_effect(vagner, state)
        self.assertAlmostEqual(0.05, df.stat_mod_pf_lv_damage_slayer)

    def test_vagner_ab6(self):
        vagner, state = self._base_state("fire_dragon")
        state.set_powerflips(2, 1)
        state.set_powerflips(3, 2)
        df = vagner.abilities[5][0].eval_effect(vagner, state)
        self.assertAlmostEqual(0.16, df.stat_mod_pf_damage)

    def test_ahanabi_ab1(self):
        ahanabi, state = self._base_state("kunoichi_1anv")
        vagner = self.wf_data.find("fire_dragon")
        sonia = self.wf_data.find("brown_fighter")
        state.set_member(vagner, CharPosition.UNISON, 0)
        state.set_member(sonia, CharPosition.MAIN, 1)

        df = ahanabi.abilities[0][0].eval_effect(ahanabi, state)
        self.assertEqual(200, df.skill_gauge_max[0])
        df = ahanabi.abilities[0][0].eval_effect(vagner, state)
        self.assertIsNone(df)

        df = ahanabi.abilities[0][1].eval_effect(ahanabi, state)
        self.assertAlmostEqual(
            0.2, df.attack_modifier, msg=f"[{ahanabi.abilities[0][1].name} | 2nd]"
        )
        df = ahanabi.abilities[0][1].eval_effect(vagner, state)
        self.assertIsNone(df)

        state.set_member(vagner, CharPosition.LEADER)
        state.set_member(ahanabi, CharPosition.UNISON, 0)
        state.ability_lvs[1][0] = 6
        df = ahanabi.abilities[0][1].eval_effect(vagner, state)
        self.assertIsNone(df)
        df = ahanabi.abilities[0][1].eval_effect(ahanabi, state)
        self.assertIsNone(df)

    def test_ahanabi_ab2(self):
        ahanabi, state = self._base_state("kunoichi_1anv")
        vagner = self.wf_data.find("fire_dragon")
        sonia = self.wf_data.find("brown_fighter")
        state.set_member(vagner, CharPosition.UNISON, 0)
        state.set_member(sonia, CharPosition.MAIN, 1)
        state.skill_activations[0] = 2
        state.skill_activations[1] = 1

        df = ahanabi.abilities[1][0].eval_effect(ahanabi, state)
        self.assertAlmostEqual(0.16, df.attack_modifier)
        df = ahanabi.abilities[1][0].eval_effect(vagner, state)
        self.assertIsNone(df)
        df = ahanabi.abilities[1][0].eval_effect(sonia, state)
        self.assertIsNone(df)

        df = ahanabi.abilities[1][1].eval_effect(ahanabi, state)
        self.assertIsNone(df)

        state.set_member(vagner, CharPosition.LEADER)
        state.set_member(ahanabi, CharPosition.UNISON, 0)
        state.ability_lvs[1][1] = 6
        df = ahanabi.abilities[1][0].eval_effect(vagner, state)
        self.assertIsNone(df)
        df = ahanabi.abilities[1][1].eval_effect(ahanabi, state)
        self.assertIsNone(df)

    def test_ahanabi_ab3(self):
        ahanabi, state = self._base_state("kunoichi_1anv")
        vagner = self.wf_data.find("fire_dragon")
        sonia = self.wf_data.find("brown_fighter")
        state.set_member(vagner, CharPosition.UNISON, 0)
        state.set_member(sonia, CharPosition.MAIN, 1)
        state.skill_charge[0] = 100
        state.times_skill_reached_100[0] = 1

        df = ahanabi.abilities[2][0].eval_effect(ahanabi, state)
        self.assertAlmostEqual(1.2, df.skill_charge_speed[0])
        df = ahanabi.abilities[2][0].eval_effect(vagner, state)
        self.assertIsNone(df)

        df = ahanabi.abilities[2][1].eval_effect(ahanabi, state)
        self.assertAlmostEqual(0.125, df.attack_modifier)
        df = ahanabi.abilities[2][1].eval_effect(vagner, state)
        self.assertIsNone(df)
        df = ahanabi.abilities[2][1].eval_effect(sonia, state)
        self.assertIsNone(df)

    def test_ahanabi_ab4(self):
        self.skipTest(
            "[AHanabi AB4] No way to test skill charge after using a "
            "skill for a non-realtime simulator."
        )

    def test_ahanabi_ab5(self):
        ahanabi, state = self._base_state("kunoichi_1anv")
        vagner = self.wf_data.find("fire_dragon")
        state.times_skill_reached_100[0] = 2
        state.times_skill_reached_100[1] = 1
        state.set_member(vagner, CharPosition.UNISON, 0)

        df = ahanabi.abilities[4][0].eval_effect(ahanabi, state)
        self.assertAlmostEqual(0.2, df.attack_modifier)
        df = ahanabi.abilities[4][0].eval_effect(vagner, state)
        self.assertIsNone(df)

        state.set_member(vagner, CharPosition.LEADER)
        state.set_member(ahanabi, CharPosition.UNISON, 0)
        state.ability_lvs[1][4] = 6
        df = ahanabi.abilities[4][0].eval_effect(vagner, state)
        self.assertAlmostEqual(0.1, df.attack_modifier)
        df = ahanabi.abilities[4][0].eval_effect(ahanabi, state)
        self.assertIsNone(df)

    def test_every_pfs_atk_this_unit(self):
        """
        Checks that the condition based on number of powerflips is working along with the effect
        that increases attack. As an extra check, this is making sure that the "this unit" target
        is working correctly by both applying the ability to the unit which benefits from the
        powerflips condition being met, and an unrelated unit.
        """
        vagner, state = self._base_state("fire_dragon")
        ahanabi = self.wf_data.find("kunoichi_1anv")
        state.set_member(ahanabi, CharPosition.UNISON, 0)
        state.set_powerflips(1, 15)

        df = vagner.abilities[1][0].eval_effect(vagner, state)
        self.assertAlmostEqual(0.45, df.attack_modifier)
        df = vagner.abilities[1][0].eval_effect(ahanabi, state)
        self.assertIs(None, df)

    def test_skill_activated_condition_ahanabi_above_cap(self):
        """
        Ensure that skill activation stacks don't go above the +attack cap for AHanabi's ability 2.
        """
        ahanabi, state = self._base_state("kunoichi_1anv")
        state.set_skill_activations(0, 20)

        df = ahanabi.abilities[1][0].eval_effect(ahanabi, state)
        self.assertAlmostEqual(0.4, df.attack_modifier)

    def test_skill_activated_condition_ahanabi_multiple_fire(self):
        """
        Ensure that skill activation stacks that apply a buff only to the unit that activated the
        skill don't take other unit skill activations into account. Specifically with AHanabi's
        ability 2.

        Puts multiple units into a party with different skill activations to ensure that each
        unit's skill activations are applied to them and them alone.
        """
        ahanabi, state = self._base_state("kunoichi_1anv")
        vagner = self.wf_data.find("Vagner")
        state.set_member(vagner, CharPosition.UNISON, 0, level=80)
        state.set_skill_activations(0, 2)
        state.set_skill_activations(1, 3)

        df = ahanabi.abilities[1][0].eval_effect(ahanabi, state)
        self.assertAlmostEqual(0.16, df.attack_modifier)

        df = ahanabi.abilities[1][0].eval_effect(vagner, state)
        self.assertIsNone(df)

    def _base_state(self, char_name: str):
        state = GameState()
        char = self.wf_data.find(char_name)
        state.set_member(char, CharPosition.LEADER, level=80)
        state.ability_lvs[0][:] = [6] * 6
        state.enemy = Enemy()
        return char, state
