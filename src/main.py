from src.simulation import Simulation
from src.subway.subway_line import SubwayLine

simulation = Simulation()

# Create a subway line and add some initial trains
line_u4 = SubwayLine("U4", 5)
line_u4.add_train()
line_u4.add_train()


simulation.add_line(line_u4)

