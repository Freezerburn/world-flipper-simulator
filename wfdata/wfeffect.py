from abc import ABC
from wfenum import Element, Buff


class Effect(ABC):
    pass


class MainEffect(Effect):
    __slots__ = ("_effect")

    def __init__(self, effect):
        self._effect = effect


class DealDamage(Effect):
    __slots__ = ("_multiplier")

    def __init__(self, multiplier: float):
        self._multiplier = multiplier


class StatBuff(Effect):
    __slots__ = ("_buff", "_element", "_amount")

    def __init__(self, element: Element, buff: Buff, amount: float):
        self._buff = buff
        self._element = element
        self._amount = amount

    def buff(self):
        return self._buff

    def element(self):
        return self._element

    def amount(self):
        return self._amount


class MultiBall(Effect):
    __slots__ = ("_number", "_time_seconds")

    def __init__(self, number: int, time_seconds: float):
        self._number = number
        self._time_seconds = time_seconds
