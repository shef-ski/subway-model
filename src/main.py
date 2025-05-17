from datetime import timedelta, datetime

from src.data.nyc_data_service import NycDataService
from src.simulation import Simulation
from src.subway.generic_subway.generic_subway_line import GenericSubwayLine
from src.animation import animate_simulation

# Create a simulation
sim = Simulation(start_time = datetime(2025, 1, 6, 8, 0), time_delta=timedelta(seconds=1))

nyc_data_service = NycDataService()
line = nyc_data_service.load_nyc_line("Crosstown")
#line = GenericSubwayLine("U4", 7)
# line.add_train()  # only add one train at the beginning, more added dynamically

# Add the line to the simulation
sim.add_line(line)

# Run with matplotlib visualization
SIMULATION_DURATION_SECONDS = 86400  # Total simulation time
ANIMATION_INTERVAL_MS = 2  # Visualization speed

animate_simulation(sim,
                   SIMULATION_DURATION_SECONDS,
                   ANIMATION_INTERVAL_MS,
                   save_video=False,
                   output_dir=".")


