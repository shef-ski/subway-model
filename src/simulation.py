from datetime import datetime, timedelta
from typing import List

from src.subway.abstract_subway_line import AbstractSubwayLine
from src.subway.event.event import Event
from src.subway.delay.delay import Delay


class Simulation:
    lines: list[AbstractSubwayLine]

    def __init__(self, start_time: datetime, time_delta: timedelta):
        self.current_time: datetime = start_time
        self.start_time: datetime = start_time
        self.timedelta = time_delta
        self.lines = []
        self.events = []
        self.breaking_times = []

        # Stores the waiting times of all passengers in seconds
        self.all_passenger_travel_times = []
        self.delays = []

    def add_line(self, line: AbstractSubwayLine):
        self.lines.append(line)

    def add_events(self, events: List[Event]):
        self.events.extend(events)

    def add_breaking_times(self, breaking_times: List[datetime]):
        self.breaking_times.extend(breaking_times)

    def add_delays(self, delays: List[Delay]):
        self.delays.extend(delays)

    def step(self):
        """Advances the simulation by one time step (1 second)."""

        for line in self.lines:
            travel_times = line.update(
                self.current_time, self.events, self.delays, self.breaking_times
            )

            if travel_times:
                self.all_passenger_travel_times += travel_times

        # Increment time for the next step
        self.current_time += self.timedelta

    def run(self, duration: int):
        """Runs the simulation without visualization."""
        for _ in range(duration):
            self.step()
