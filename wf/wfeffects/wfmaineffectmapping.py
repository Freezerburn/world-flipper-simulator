from .wfmainconditions import *
from .wfmaineffects import *

main_condition_mapping: dict[str, Type[WorldFlipperCondition]] = {
    "0": OnBattleStartMainCondition,
    "1": NTimesCondition("ability_description_instant_trigger_kind_power_flip"),
    "100": NTimesCondition("ability_description_instant_trigger_kind_skill_hit"),
    # "13": None,
    # "131": None,
    # "132": None,
    # "136": None,
    # "137": None,
    # "14": None,
    # "15": None,
    # "16": None,
    "18": OnSkillInvokeMainCondition,
    "19": OnSkillGaugeReach100MainCondition,
    # "2": None,
    # "20": None,
    # "22": None,
    # "23": None,
    "24": OnAttackBuffActivateCondition,
    "3": NTimesCondition("ability_description_instant_trigger_kind_ball_flip"),
    # "4": ["ability_description_instant_trigger_kind_fever"],
    "4": InFeverCondition,
    # "45": None,
    # "46": None,
    # "5": None,
    "50": PartyMembersAddedMainCondition,
    # "51": None,
    # "56": None,
    # "57": None,
    "58": Lv3PowerFlipsMainCondition,
    # "59": None,
    # "6": ["ability_description_instant_trigger_kind_enemy_kill"],
    # "63": None,
    "7": ComboReachedMainCondition,
    # "70": None,
    # "8": None,
}

main_effect_mapping: dict[str, list[Type[WorldFlipperEffect]]] = {
    "0": [
        ActiveForSecondsMainEffect,
        AttackMainEffect,
    ],
    "1": [SkillDamageMainEffect],
    # NOTE: Currently this is hard-coded to Fire Resistance Debuff. Only AHanabi has this.
    "107": [FireResistDebuffSlayerMainEffect],
    "112": [],
    "116": [PoisonSlayerMainEffect],
    "117": [],
    "118": [SlowDebuffSlayerMainEffect],
    "123": [],
    "144": [PoisonDirectAttackMainEffect],
    # NOTE: This ALWAYS uses Power Flip Lv3.
    "152": [Lv3PowerFlipDamageMainEffect],
    "155": [],
    # NOTE: This ALWAYS sets "Attack Buff" as the condition.
    "156": [AttackBuffExtendMainEffect],
    "158": [],
    "16": [],
    "162": [],
    "164": [],
    "17": [],
    "176": [],
    "189": [],
    "190": [],
    "191": [],
    "193": [],
    "195": [],
    "196": [],
    "198": [PowerFlipComboCountDownMainEffect],
    "199": [],
    "2": [],
    "201": [],
    "203": [IncreaseHpMainEffect],
    "204": [],
    "207": [],
    "209": [IncreaseSkillChargeMainEffect],
    "21": [],
    "211": [],
    "212": [],
    "218": [],
    "221": [],
    "222": [],
    "224": [IncreaseComboMainEffect],
    "225": [],
    "24": [],
    "243": [SecondSkillGaugeMainEffect],
    "245": [],
    "249": [NoOpMainEffect(["ability_description_instant_content_enemy_damage"])],
    "251": [],
    "253": [],
    "26": [
        ActiveForSecondsMainEffect,
        PierceMainEffect,
    ],
    "265": [],
    "27": [],
    "28": [
        ActiveForSecondsMainEffect,
        PowerFlipDamageMainEffect,
    ],
    "289": [],
    "307": [],
    "31": [AttackMainEffect],
    "32": [],
    "33": [SkillDamageMainEffect],
    "330": [],
    "34": [],
    "35": [],
    "354": [],
    "36": [ResistUpMainEffect],
    "366": [],
    "37": [],
    "38": [],
    "386": [],
    "388": [],
    "389": [],
    "39": [],
    "391": [],
    "4": [],
    "40": [],
    "41": [],
    "411": [],
    "459": [],
    "460": [],
    "466": [],
    "468": [],
    "487": [],
    "489": [],
    "49": [FeverGainRateMainEffect],
    "5": [],
    "50": [],
    "501": [],
    "503": [],
    "504": [],
    "505": [],
    "506": [],
    "51": [],
    "510": [PoisonAttackMainEffect],
    "512": [],
    "518": [],
    "52": [],
    "522": [],
    "525": [],
    "533": [],
    "54": [PowerFlipDamageMainEffect],
    "55": [],
    "58": [],
    "61": [],
    "66": [],
    "67": [],
    "68": [],
    "69": [],
    "7": [],
    "8": [],
    "95": [],
    "98": [],
}
