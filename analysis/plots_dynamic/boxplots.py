import matplotlib.pyplot as plt
import numpy as np

from tools.simulation_runner import SimulationRunner


def boxplots(runner: SimulationRunner):
    """
    Plots side-by-side boxplots for each capacity level in the given SimulationRunner.

    - Left plot: Utilization rates
    - Right plot: Travel times

    Args:
        runner (SimulationRunner): The simulation runner object with results.
    """
    # Get sorted list of capacities
    capacities = sorted(runner.all_util_rates.keys())

    # Gather data for boxplots
    util_data = [runner.all_util_rates[cap] for cap in capacities]
    travel_time_data = [runner.all_travel_times[cap] for cap in capacities]

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Utilization boxplots
    axs[0].boxplot(util_data, positions=np.arange(len(capacities)), patch_artist=True)
    axs[0].set_title(
        f"Utilization Rates ({runner.line_name})", fontsize=14, fontweight="bold"
    )
    axs[0].set_xticks(np.arange(len(capacities)))
    axs[0].set_xticklabels([str(cap) for cap in capacities])
    axs[0].set_xlabel("Capacity")
    axs[0].set_ylabel("Utilization Rate")

    # Travel time boxplots
    axs[1].boxplot(
        travel_time_data, positions=np.arange(len(capacities)), patch_artist=True
    )
    axs[1].set_title(
        f"Travel Times ({runner.line_name})", fontsize=14, fontweight="bold"
    )
    axs[1].set_xticks(np.arange(len(capacities)))
    axs[1].set_xticklabels([str(cap) for cap in capacities])
    axs[1].set_xlabel("Capacity")
    axs[1].set_ylabel("Travel Time (minutes)")

    fig.suptitle(
        f"Simulation Distributions by Capacity ({runner.line_name})",
        fontsize=16,
        fontweight="bold",
    )
    plt.tight_layout(rect=(0, 0, 1, 0.96))  # was list before
    plt.show()
