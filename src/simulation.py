from constants import TRAVEL_TIME_BETWEEN_STATIONS, DWELL_TIME_AT_STATION

from src.subway.subway_line import SubwayLine


class Simulation:

    def __init__(self):
        self.current_time: int = 0  # Simulation time in minutes
        self.trains = []
        self.lines = []
        # Add other components like passengers later if needed

    def add_line(self, line: SubwayLine):
        self.lines.append(line)

    def step(self):
        """Advances the simulation by one time step (1 minute)."""
        print(f"\n--- Minute {self.current_time} ---")

        for line in self.lines:
            for train in line.trains:
                train.update(self.current_time)

        # Update other components (e.g., passenger arrivals at stations) later

        # Increment time for the next step
        self.current_time += 1

    def run(self, duration: int):
        """Runs the simulation for a given duration in minutes."""
        print(f"=== Starting Simulation (Duration: {duration} minutes) ===")
        print(f"Travel time between stations: {TRAVEL_TIME_BETWEEN_STATIONS} min")
        print(f"Dwell time at stations: {DWELL_TIME_AT_STATION} min")
        for _ in range(duration):
            self.step()
        print(f"\n=== Simulation Finished at Minute {self.current_time - 1} ===")
