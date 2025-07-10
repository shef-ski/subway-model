import random
from datetime import datetime, timedelta

from analysis.plots_dynamic.capacity_tradeoff import capacity_tradeoff_plot
from analysis.plots_dynamic.distribution_plots import create_distribution_plot
from analysis.plots_dynamic.histogram import utilization_histogram
from analysis.plots_dynamic.regular_plots import create_basic_plot
from src.subway.event.event import Event
from src.subway.delay.delay import Delay
from tools.simulation_runner import SimulationRunner


# run this code from the project root using:
# python -m analysis.run_simulations

# --- Set constant parameters for the experiment ---
SEED = 1234
random.seed(SEED)

N_RUNS = 3
DURATION = 5400  # 5400s = 90min

CAPACITIES = [200, 500, 800, 1200]

SIM_START_TIME = datetime(2025, 1, 6, 7, 30)
SIM_TIME_DELTA = timedelta(seconds=1)

LINE_NAME = "Lexington Av-6"

SAVE_OUTPUTS = True
SAVE_PATH = "analysis/outputs/"

ADD_BREAKING_TIMES = False
ADD_EVENTS = True
ADD_DELAY = False


# --- Run the simulation ---
simulation_runner = SimulationRunner(
    N_RUNS, DURATION, CAPACITIES, SIM_START_TIME, SIM_TIME_DELTA, LINE_NAME
)

# OPTIONAL: Add times [t1, t2, ...] at which a (pseudo-)random train breaks
breaking_times = []
if ADD_BREAKING_TIMES:
    breaking_times.append(SIM_START_TIME + timedelta(minutes=15))
    breaking_times.append(SIM_START_TIME + timedelta(minutes=22))
    breaking_times.append(SIM_START_TIME + timedelta(minutes=30))

# OPTIONAL: Create basic event which temporarily increases ridership
events = []
if ADD_EVENTS:
    event_start_time = SIM_START_TIME + timedelta(minutes=35)
    event_end_time = event_start_time + timedelta(hours=1)
    event = Event("show", 5, 20000, event_start_time, event_end_time)
    events.append(event)

# OPTIONAL: Create delay
delays = []
if ADD_DELAY:
    delay_start_time = SIM_START_TIME + timedelta(minutes=20)
    delay_end_time = delay_start_time + timedelta(minutes=10)
    delay = Delay("coffee", 5, delay_start_time, delay_end_time)
    delays.append(delay)

# Adapt inputs
simulation_runner.run_simulations(breaking_times, events, delays)

if SAVE_OUTPUTS:
    simulation_runner.save_outputs(SAVE_PATH)


# --- Make visualizations ---
# this should also work with the saved outputs from above

capacity_tradeoff_plot(
    simulation_runner.all_util_rates, simulation_runner.all_travel_times
)

# create_distribution_plot(simulation_runner.df_avg_util_rates)

# utilization_histogram(simulation_runner.all_util_rates)

# create_basic_plot(simulation_runner.average_util_rates)
