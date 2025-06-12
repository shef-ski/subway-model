from analysis.plots_dynamic.boxplots import boxplots
from analysis.plots_dynamic.capacity_tradeoff import plot_tradeoff_curves
from analysis.plots_dynamic.distribution_plots import create_distribution_plot
from analysis.plots_dynamic.histogram import utilization_histogram
from analysis.plots_dynamic.regular_plots import create_basic_plot
from tools.simulation_runner import SimulationRunner


BASE_PATH = "analysis/outputs/"

LOAD_PATHS = [
    # "sim_FFF_20250612_215109",
    "sim_TTT_20250612_220221",
    #  "sim_FTF_20250612_221057",
    #  "sim_TFT_20250612_221512",
    #  "sim_FTF_20250612_223739_large",
]

sim_runners = []

for sim_path in LOAD_PATHS:
    simulation_runner = SimulationRunner.from_saved(BASE_PATH, sim_path)

    sim_runners.append(simulation_runner)


plot_tradeoff_curves(sim_runners)


boxplots(sim_runners[0])
