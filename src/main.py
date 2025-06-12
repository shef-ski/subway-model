from datetime import timedelta, datetime
import random

from src.animation.animation_1d import animate_simulation_1d
from src.animation.animation_2d import animate_simulation_2d
from src.data.nyc_data_service import NycDataService
from src.data.nyc_map import NycMap
from src.simulation import Simulation
from src.subway.event.event import Event
from src.subway.delay.delay import Delay
from src.subway.generic_subway.generic_subway_line import GenericSubwayLine

# --- Constants ---
SEED = 12345
random.seed(SEED)

ADD_BREAKING_TIMES = False
ADD_EVENTS = False
ADD_DELAY = False

SIM_START_TIME = datetime(2025, 1, 6, 8, 0)

SIMULATION_DURATION_SECONDS = 180  # = 4h
ANIMATION_INTERVAL_MS = 2  # Visualization speed
ANIMATE_2D = True
SAVE_VIDEO = False

# --- Simulation ---
# Create a simulation object
sim = Simulation(start_time=SIM_START_TIME, time_delta=timedelta(seconds=1))

# Create a subway line and a corresponding map
nyc_data_service = NycDataService()
line = nyc_data_service.load_nyc_line("Lexington Av-6")
map = NycMap(NycDataService.SHAPE_PATH, line)

# line = GenericSubwayLine("U4", 3, 500)

# Add the line to the simulation
sim.add_line(line)

# OPTIONAL: Add times [t1, t2, ...] at which a (pseudo-)random train breaks
if ADD_BREAKING_TIMES:
    train_breaking_times = []
    train_breaking_times.append(SIM_START_TIME + timedelta(minutes=60))
    train_breaking_times.append(SIM_START_TIME + timedelta(minutes=70))
    train_breaking_times.append(SIM_START_TIME + timedelta(minutes=80))
    sim.add_breaking_times(train_breaking_times)

# OPTIONAL: Create basic event which temporarily increases ridership
if ADD_EVENTS:
    event_start_time = SIM_START_TIME + timedelta(minutes=120)
    event_end_time = event_start_time + timedelta(hours=1)
    event = Event("show", 5, 3000, event_start_time, event_end_time)
    sim.add_events([event])

# OPTIONAL: Create delay
if ADD_DELAY:
    delay_start_time = SIM_START_TIME + timedelta(minutes=210)
    delay_end_time = delay_start_time + timedelta(minutes=10)
    delay = Delay("coffee", 5, delay_start_time, delay_end_time)
    sim.add_delays([delay])

# --- Animation ---
if ANIMATE_2D:
    animate_simulation_2d(
        sim,
        map,
        SIMULATION_DURATION_SECONDS,
        ANIMATION_INTERVAL_MS,
        save_video=SAVE_VIDEO,
        output_dir=".",
        trim_to_square=True,
    )
else:
    animate_simulation_1d(
        sim,
        SIMULATION_DURATION_SECONDS,
        ANIMATION_INTERVAL_MS,
        save_video=SAVE_VIDEO,
        output_dir=".",
    )
