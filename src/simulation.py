from src.subway.subway_line import SubwayLine


class Simulation:
    # lines: list[SubwayLine]

    def __init__(self):
        self.current_time: int = 0  # Simulation time in minutes
        self.lines = []

    def add_line(self, line: SubwayLine):
        self.lines.append(line)

    def step(self):
        """Advances the simulation by one time step (1 second)."""

        for line in self.lines:
            line.update(self.current_time)

            if self.current_time == 240 or self.current_time == 480:
                line.add_train()

            for station in line.stations:
                station.random_psg_arrival()

        # Increment time for the next step
        self.current_time += 1

    def run(self, duration: int):
        """Runs the simulation without visualization."""
        for _ in range(duration):
            self.step()
