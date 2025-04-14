from constants import TRAVEL_TIME_BETWEEN_STATIONS, DWELL_TIME_AT_STATION

from src.subway.subway_line import SubwayLine


class Simulation:

    def __init__(self):
        self.current_time: int = 0  # Simulation time in minutes
        self.lines = []

    def add_line(self, line: SubwayLine):
        self.lines.append(line)

    def step(self):
        """Advances the simulation by one time step (1 second)."""

        for line in self.lines:
            line.update(self.current_time)

            for station in line.stations:
                station.random_psg_arrival()


        # Increment time for the next step
        self.current_time += 1

    def run(self, duration: int):
        """Runs the simulation without visualization."""
        for _ in range(duration):
            self.step()
