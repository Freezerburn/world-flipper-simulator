from unittest import TestCase

from wf import WorldFlipperData, CharPosition, DamageFormulaContext
from wf.wfenemy import Enemy
from wf.wfgamestate import GameState


class TestWorldFlipperAbility(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wf_data = WorldFlipperData("wf_data_json")

    def test_skill_activated_condition_ahanabi_above_cap(self):
        """
        Ensure that skill activation stacks don't go above the +attack cap for AHanabi's ability 2.
        """
        ahanabi, state = self._base_state("kunoichi_1anv")
        state.set_skill_activations(0, 20)

        df = ahanabi.abilities[1][0].eval_effect(ahanabi, state)
        self.assertEqual(0.4, df.attack_modifier)

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
        self.assertEqual(0.16, df.attack_modifier)

        df = ahanabi.abilities[1][0].eval_effect(vagner, state)
        self.assertEqual(0.24, df.attack_modifier)

    def _base_state(self, char_name: str):
        state = GameState()
        char = self.wf_data.find(char_name)
        state.set_member(char, CharPosition.LEADER, level=80)
        state.ability_lvs[0][:] = [6] * 6
        state.enemy = Enemy()
        return char, state
