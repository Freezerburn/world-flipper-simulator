from wfdata import wfenum
from wfdata.wfeffect import Effect, StatBuff, DealDamage
from wfdata.wfdmgformula import DamageFormulaContext

from wfchar import Character


class Vagner(Character):
    def __init__(self, char_json):
        super().__init__(char_json)
        self.skill_multiplier = 27
        self.total_power_flips = 0
        self.total_lv3_power_flips = 0

    def image(self) -> str:
        return "fire_dragon.png"

    def name(self) -> str:
        return "Vagner"

    def leader_text(self) -> str:
        return "[Throne of Fire] Fire characters' ATK +100% / Power flip damage +70%"

    def skill_text(self) -> str:
        return ("[Prominence Blaze] With a breath of blazing fire, deal fire damage (27x) towards the front to enemies "
                "hit")

    def ability_text(self) -> [str]:
        return [
            "Power flip damage +30%",
            "Every 5 power flips, own ATK +15% [MAX: +90%]",
            "[Main] Combo required for Lv3 power flip -5 and power flip damage +40%",
            "When battle begins, own skill gauge +50%",
            "Combo required for Lv3 power flip -2 and Lv3 power flip damage +5%",
            "Every Lv3 power flip, power flip damage +8% [MAX: +40%]"
        ]

    def leader_effects(self):
        return [
            StatBuff(wfenum.Element.FIRE, wfenum.Buff.ATTACK, 1),
            StatBuff(wfenum.Element.FIRE, wfenum.Buff.POWER_FLIP, 0.7)
        ]

    def skill_effects(self) -> [Effect]:
        return [
            DealDamage(27)
        ]

    def skill_cost(self):
        if self.evolved:
            return self.skill_evolve_cost
        return self.skill_base_cost

    def damage_contexts(self) -> [DamageFormulaContext]:
        leader_ctx = DamageFormulaContext()
        leader_ctx.element = wfenum.Element.FIRE
        leader_ctx.attack_modifier = 1
        leader_ctx.stat_mod_pf_damage = 0.7

        a1_ctx = DamageFormulaContext()
        a1_ctx.stat_mod_pf_damage = 0.3

        a2_ctx = DamageFormulaContext()
        a2_ctx.target_character = self.name()
        power_flips = self.total_power_flips
        while power_flips >= 5 and a2_ctx.attack_modifier < 0.9:
            a2_ctx.attack_modifier += 0.15
            power_flips -= 5

        a3_ctx = DamageFormulaContext()
        a3_ctx.requires_main = True
        a3_ctx.stat_mod_pf_damage = 0.4

        # a4 ctx is only to increase skill charge, so there's no damage modification to return.

        a5_ctx = DamageFormulaContext()
        a5_ctx.stat_mod_pf_lv_damage_slayer_lv = 3
        a5_ctx.stat_mod_pf_lv_damage_slayer = 0.05

        a6_ctx = DamageFormulaContext()
        if 0 <= self.total_lv3_power_flips <= 5:
            a5_ctx.stat_mod_pf_damage = self.total_lv3_power_flips * 0.08
        else:
            a5_ctx.stat_mod_pf_damage = 0.4

        return [leader_ctx, a1_ctx, a2_ctx, a3_ctx, a5_ctx, a6_ctx]
