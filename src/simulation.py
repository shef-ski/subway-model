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

        # todo Update other components (e.g., passenger arrivals at stations)

        # Increment time for the next step
        self.current_time += 1

    def run(self, duration: int):
        """Runs the simulation for a given duration in minutes (without visualization!)"""
        print(f"=== Starting Simulation (Duration: {round(duration/60)} minutes) ===")
        print(f"Travel time between stations: {TRAVEL_TIME_BETWEEN_STATIONS} seconds")
        print(f"Dwell time at stations: {DWELL_TIME_AT_STATION} seconds")
        for _ in range(duration):
            self.step()
        print(f"\n=== Simulation Finished at Minute {self.current_time - 1} ===")
