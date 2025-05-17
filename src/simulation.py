from datetime import datetime, timedelta

from src.subway.abstract_subway_line import AbstractSubwayLine


class Simulation:
    lines: list[AbstractSubwayLine]

    def __init__(self, start_time: datetime, time_delta: timedelta):
        self.current_time: datetime = start_time  # Simulation time in minutes
        self.start_time: datetime = start_time
        self.timedelta = time_delta
        self.lines = []

    def add_line(self, line: AbstractSubwayLine):
        self.lines.append(line)

    def step(self):
        """Advances the simulation by one time step (1 second)."""

        for line in self.lines:
            line.update(self.current_time)
            elapsed_seconds = (self.current_time - self.start_time).total_seconds()
            # For now, add trains every 4 minutes and have max 5 --> todo: make this more intelligent
            if elapsed_seconds % 240 == 0 and len(line.get_trains()) < 5:
                line.add_train()

        # Increment time for the next step
        self.current_time += self.timedelta

    def run(self, duration: int):
        """Runs the simulation without visualization."""
        for _ in range(duration):
            self.step()
