from src.subway.abstract_subway_line import AbstractSubwayLine


class Simulation:
    lines: list[AbstractSubwayLine]

    def __init__(self, capacity: int = 500):
        self.capacity = capacity
        self.current_time: int = 0  # Simulation time in minutes
        self.lines = []

    def add_line(self, line: AbstractSubwayLine):
        self.lines.append(line)

    def step(self, capacity):
        """Advances the simulation by one time step (1 second)."""
        self.capacity = capacity
        for line in self.lines:
            line.update(self.current_time)

            # For now, add trains every 4 minutes and have max 5 --> todo: make this more intelligent
            if self.current_time % 240 == 0 and len(line.get_trains()) < 5:
                line.add_train(capacity=self.capacity)

        # Increment time for the next step
        self.current_time += 1

    def run(self, duration: int):
        """Runs the simulation without visualization."""
        for _ in range(duration):
            self.step()
