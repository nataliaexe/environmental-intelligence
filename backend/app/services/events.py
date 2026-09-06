from collections import deque

from app.domain.event import EnvironmentalEvent


class EventStore:
    def __init__(self, max_size: int = 1000) -> None:
        self._events: deque[EnvironmentalEvent] = deque(
            maxlen=max_size
        )

    def add(self, event: EnvironmentalEvent) -> None:
        self._events.append(event)

    def all(self) -> list[EnvironmentalEvent]:
        return list(self._events)

    def active(self) -> list[EnvironmentalEvent]:
        return [
            event
            for event in self._events
            if event.status == "active"
        ]

    def by_region(
        self,
        region_id: str,
    ) -> list[EnvironmentalEvent]:
        return [
            event
            for event in self._events
            if event.region_id == region_id
        ]


event_store = EventStore()
