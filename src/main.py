from src.data.nyc_data_service import NycDataService
from src.simulation import Simulation
from src.subway.generic_subway.generic_subway_line import GenericSubwayLine
from src.animation import animate_simulation

# Create a simulation
sim = Simulation()

nyc_data_service = NycDataService()
#line = nyc_data_service.load_nyc_line("Crosstown")
line = GenericSubwayLine("U4", 7)
# line.add_train()  # only add one train at the beginning, more added dynamically

# Add the line to the simulation
sim.add_line(line)

# Run with matplotlib visualization
SIMULATION_DURATION_SECONDS = 2000  # Total simulation time
ANIMATION_INTERVAL_MS = 20  # Visualization speed

animate_simulation(sim,
                   SIMULATION_DURATION_SECONDS,
                   ANIMATION_INTERVAL_MS,
                   save_video=False,
                   output_dir=".")


