import random
from datetime import datetime, timedelta

from analysis.plots_dynamic.capacity_tradeoff import capacity_tradeoff_plot
from analysis.plots_dynamic.distribution_plots import create_distribution_plot
from analysis.plots_dynamic.histogram import utilization_histogram
from analysis.plots_dynamic.regular_plots import create_basic_plot
from src.subway.event.event import Event
from tools.simulation_runner import SimulationRunner


# run this code from the project root using:
# python -m analysis.main

# --- Set constant parameters for the experiment ---
SEED = 12345
random.seed(SEED)

N_RUNS = 3
DURATION = 3600

CAPACITIES = [100, 300, 500, 1000]

SIM_START_TIME = datetime(2025, 1, 6, 8, 0)
SIM_TIME_DELTA = timedelta(seconds=1)

LINE_NAME = "Lexington Av-6"

SAVE_OUTPUTS = False
SAVE_PATH = "analysis/outputs/"

ADD_BREAKING_TIMES = True
ADD_EVENTS = True


# --- Run the simulation ---
simulation_runner = SimulationRunner(N_RUNS,
                                     DURATION,
                                     CAPACITIES,
                                     SIM_START_TIME,
                                     SIM_TIME_DELTA,
                                     LINE_NAME)

# OPTIONAL: Add times [t1, t2, ...] at which a (pseudo-)random train breaks
train_breaking_times = []
if ADD_BREAKING_TIMES:
    train_breaking_times.append(SIM_START_TIME + timedelta(minutes=15))
    train_breaking_times.append(SIM_START_TIME + timedelta(minutes=22))
    train_breaking_times.append(SIM_START_TIME + timedelta(minutes=30))

# OPTIONAL: Create basic event which temporarily increases ridership
events = []
if ADD_EVENTS:
    event_start_time = SIM_START_TIME + timedelta(minutes=30)
    event_end_time = event_start_time + timedelta(hours=1)
    event = Event("show", 5, 3000, event_start_time, event_end_time)
    events.append(event)

# Adapt inputs
simulation_runner.run_simulations(train_breaking_times,
                                  events)


if SAVE_OUTPUTS:
    # todo
    # the dicts which store the data should be saveable as csv somehow
    simulation_runner.save_outputs_to_csv(SAVE_PATH)


# --- Make visualizations ---
# this should also work with the saved outputs from above

capacity_tradeoff_plot(simulation_runner.all_util_rates, simulation_runner.all_travel_times)

create_distribution_plot(simulation_runner.df_avg_util_rates)

utilization_histogram(simulation_runner.all_util_rates)

create_basic_plot(simulation_runner.average_util_rates)

