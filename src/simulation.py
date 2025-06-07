from datetime import datetime, timedelta
from typing import List

from src.subway.abstract_subway_line import AbstractSubwayLine
from src.subway.event.event import Event


class Simulation:
    lines: list[AbstractSubwayLine]

    def __init__(self,
                 start_time: datetime,
                 time_delta: timedelta,
                 capacity: int = 500):
        self.current_time: datetime = start_time  # Simulation time in minutes
        self.start_time: datetime = start_time
        self.timedelta = time_delta
        self.capacity = capacity
        self.lines = []
        self.events = []

    def add_line(self, line: AbstractSubwayLine):
        self.lines.append(line)

    def add_events(self, events: List[Event]):
        self.events.extend(events)

    def step(self):
        """Advances the simulation by one time step (1 second)."""

        for line in self.lines:
            line.update(self.current_time, self.events)

        # Increment time for the next step
        self.current_time += self.timedelta

    def run(self, duration: int):
        """Runs the simulation without visualization."""
        for _ in range(duration):
            self.step()
