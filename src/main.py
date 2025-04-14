from src.simulation import Simulation
from src.subway.subway_line import SubwayLine
from visualization import animate_simulation

# Create a simulation
sim = Simulation()

# Create a subway line and add some initial trains
line = SubwayLine("U4", 5)
line.add_train()
line.add_train()

# Add the line to the simulation
sim.add_line(line)

# Run with matplotlib visualization
SIMULATION_DURATION_SECONDS = 2000  # Total simulation time
ANIMATION_INTERVAL_MS = 20  # Visualization speed

animate_simulation(sim, SIMULATION_DURATION_SECONDS, ANIMATION_INTERVAL_MS)



