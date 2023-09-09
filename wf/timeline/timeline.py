from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .events import Event


class WorldFlipperTimeline:
    def __init__(self):
        self._events: list[Event] = []

    def add_event(self, event: Event):
        added = False
        for i, e in enumerate(self._events):
            if event.time_activated < e.time_activated:
                self._events.insert(i, event)
                added = True
                break
        if not added:
            self._events.append(event)
