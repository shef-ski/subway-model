from datetime import timedelta, datetime
import random

from src.animation.animation_1d import animate_simulation_1d
from src.animation.animation_2d import animate_simulation_2d
from src.data.nyc_data_service import NycDataService
from src.data.nyc_map import NycMap
from src.simulation import Simulation
from src.subway.event.event import Event
from src.subway.delay.delay import Delay


seed = 12345
random.seed(seed)

# Create a simulation
start_time = datetime(2025, 2, 4, 6, 0)
sim = Simulation(start_time=start_time, time_delta=timedelta(seconds=1))

delay_start_time = start_time + timedelta(minutes=10)
delay_end_time = delay_start_time + timedelta(minutes=10)

# Create delay
delay = Delay("coffee", 5, delay_start_time, delay_end_time)

# Create a subway line and a corresponding map
nyc_data_service = NycDataService()
line = nyc_data_service.load_nyc_line("Lexington Av-6")
map = NycMap(NycDataService.SHAPE_PATH, line)

# Add the line to the simulation
sim.add_line(line)

# OPTIONAL: Add times [t1, t2, ...] at which a (pseudo-)random train breaks
train_breaking_times = []
train_breaking_times.append(start_time + timedelta(minutes=45))
train_breaking_times.append(start_time + timedelta(minutes=62))
train_breaking_times.append(start_time + timedelta(minutes=70))
sim.add_breaking_times(train_breaking_times)

# OPTIONAL: Create basic event which temporarily increases ridership
event_start_time = start_time + timedelta(minutes=30)
event_end_time = event_start_time + timedelta(hours=1)
event = Event("show", 5, 3000, event_start_time, event_end_time)
# sim.add_events([event])
sim.add_delays([delay])

# Run with matplotlib visualization
SIMULATION_DURATION_SECONDS = 160000  # Total simulation time
ANIMATION_INTERVAL_MS = 2  # Visualization speed
ANIMATE_2D = True

if ANIMATE_2D:
    # requires a NycMap object
    animate_simulation_2d(
        sim,
        map,
        SIMULATION_DURATION_SECONDS,
        ANIMATION_INTERVAL_MS,
        save_video=False,
        output_dir=".",
        trim_to_square=True,
    )

else:
    animate_simulation_1d(
        sim,
        SIMULATION_DURATION_SECONDS,
        ANIMATION_INTERVAL_MS,
        save_video=False,
        output_dir=".",
    )
