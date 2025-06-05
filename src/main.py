from datetime import timedelta, datetime

from src.animation.animation_2d import animate_simulation_2d
from src.data.nyc_data_service import NycDataService
from src.data.nyc_map import NycMap
from src.simulation import Simulation
from src.subway.generic_subway.generic_subway_line import GenericSubwayLine
from src.animation.animation_1d import animate_simulation_1d

# Create a simulation
sim = Simulation(start_time = datetime(2025, 1, 6, 8, 0), time_delta=timedelta(seconds=1))

# Create a subway line and a corresponding map
nyc_data_service = NycDataService()
line = nyc_data_service.load_nyc_line("Lexington Av")
map = NycMap(NycDataService.SHAPE_PATH, line)
#line = GenericSubwayLine("U4", 7)


# Add the line to the simulation
sim.add_line(line)

# Run with matplotlib visualization
SIMULATION_DURATION_SECONDS = 160000  # Total simulation time
ANIMATION_INTERVAL_MS = 2  # Visualization speed
ANIMATE_2D = True

if ANIMATE_2D:
    # requires a NycMap object
    animate_simulation_2d(sim,
                          map,
                          SIMULATION_DURATION_SECONDS,
                          ANIMATION_INTERVAL_MS,
                          save_video=False,
                          output_dir=".",
                          trim_to_square=True)

else:
    animate_simulation_1d(sim,
                          SIMULATION_DURATION_SECONDS,
                          ANIMATION_INTERVAL_MS,
                          save_video=False,
                          output_dir=".")
