from analysis.plots_dynamic.capacity_tradeoff import plot_tradeoff_curves
from analysis.plots_dynamic.distribution_plots import create_distribution_plot
from analysis.plots_dynamic.histogram import utilization_histogram
from analysis.plots_dynamic.regular_plots import create_basic_plot
from tools.simulation_runner import SimulationRunner


BASE_PATH = "analysis/outputs/"

LOAD_PATHS = [
    "sim_FFF_20250612_184327", 
    "sim_TTT_20250612_190145"
    ]

sim_runners = []

for sim_path in LOAD_PATHS:

    simulation_runner = SimulationRunner.from_saved(BASE_PATH, sim_path)

    sim_runners.append(simulation_runner)


plot_tradeoff_curves(sim_runners)
