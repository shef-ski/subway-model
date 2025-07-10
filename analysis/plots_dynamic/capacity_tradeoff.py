import matplotlib.pyplot as plt
import numpy as np
from typing import List

from tools.simulation_runner import SimulationRunner


def _plot_single_tradeoff_curve(
    ax, all_util_rates: dict, all_travel_times: dict, label: str, color: str
):
    """
    Helper function to plot a single tradeoff curve on a given Matplotlib Axes.

    Args:
        ax (matplotlib.axes.Axes): The axes object to draw the plot on.
        all_util_rates (dict): Dictionary of utilization rates for one simulation.
        all_travel_times (dict): Dictionary of travel times for one simulation.
        label (str): The label for this specific curve in the legend.
        color (str): The color to use for this curve.
    """
    inverse_util_rates = {
        cap: [1 - r for r in rates] for cap, rates in all_util_rates.items()
    }
    sorted_capacities = sorted(inverse_util_rates.keys())

    avg_emptiness_rates = [
        np.mean(inverse_util_rates[cap]) for cap in sorted_capacities
    ]
    avg_travel_times = [np.mean(all_travel_times[cap]) for cap in sorted_capacities]

    # Plot the curve on the provided axes object
    ax.plot(
        avg_travel_times,
        avg_emptiness_rates,
        marker="o",
        linestyle="-",
        color=color,
        label=label,
    )

    # Annotate each point with its capacity value
    for i, capacity in enumerate(sorted_capacities):
        ax.annotate(
            f"C={capacity}",
            (avg_travel_times[i], avg_emptiness_rates[i]),
            textcoords="offset points",
            xytext=(0, -15),  # Position text below the point to avoid overlap
            ha="center",
            fontsize=8,
            color=color,
            alpha=0.8,
        )


def _plot_single_tradeoff_curve2(
    ax, all_util_rates: dict, all_travel_times: dict, label: str, color: str
):
    import numpy as np

    inverse_util_rates = {
        cap: [1 - r for r in rates] for cap, rates in all_util_rates.items()
    }
    sorted_capacities = sorted(inverse_util_rates.keys())

    avg_emptiness_rates = []
    std_emptiness_rates = []
    avg_travel_times = []
    std_travel_times = []

    for cap in sorted_capacities:
        empties = inverse_util_rates[cap]
        times = all_travel_times[cap]
        avg_emptiness_rates.append(np.mean(empties))
        std_emptiness_rates.append(np.std(empties))
        avg_travel_times.append(np.mean(times))
        std_travel_times.append(np.std(times))

    # Main line:
    ax.plot(
        avg_travel_times,
        avg_emptiness_rates,
        marker="o",
        linestyle="-",
        color=color,
        label=label,
    )

    # Subtle shaded bands for deviation (95% confidence or 1 std)
    ax.fill_between(
        avg_travel_times,
        np.array(avg_emptiness_rates) - np.array(std_emptiness_rates),
        np.array(avg_emptiness_rates) + np.array(std_emptiness_rates),
        color=color,
        alpha=0.15,
        linewidth=0,
        zorder=0,
    )

    # Annotations for clarity (optional)
    for i, capacity in enumerate(sorted_capacities):
        ax.annotate(
            f"C={capacity}",
            (avg_travel_times[i], avg_emptiness_rates[i]),
            textcoords="offset points",
            xytext=(0, -12),
            ha="center",
            fontsize=8,
            color=color,
            alpha=0.9,
        )


def plot_tradeoff_curves(runners: List[SimulationRunner]):
    """
    Creates a single plot with multiple tradeoff curves, one for each SimulationRunner.

    This function visualizes the tradeoff between system utilization and travel time
    for several different simulation scenarios, plotting them on the same graph for
    easy comparison.

    Args:
        runners (List[SimulationRunner]): A list of SimulationRunner instances,
                                           each containing its own simulation results.
    """
    if not runners:
        print("The list of runners cannot be empty.")
        return

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(12, 8))

    # A list of distinct colors to cycle through for the plots
    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
    ]

    for i, runner in enumerate(runners):
        if not runner.all_util_rates or not runner.all_travel_times:
            print(
                f"Warning: Skipping runner '{runner.line_name}' due to empty result data."
            )
            continue

        # Use the runner's metadata to create an informative label
        label = f"Line: {runner.line_name} ({runner.n_runs} runs)"
        label = f"{runner.description}"

        # Cycle through colors using the modulo operator
        color = colors[i % len(colors)]

        # Call the helper function to do the actual plotting
        _plot_single_tradeoff_curve(
            ax=ax,
            all_util_rates=runner.all_util_rates,
            all_travel_times=runner.all_travel_times,
            label=label,
            color=color,
        )

    # --- Final Formatting for the Combined Plot ---
    ax.set_title(
        "Capacity Tradeoff Comparison: 2 Types of Waste", fontsize=16, fontweight="bold"
    )
    ax.set_xlabel("Average Passenger Travel Duration in Minutes", fontsize=12)
    ax.set_ylabel("Average Train Emptiness Rate (1 - Utilization)", fontsize=12)
    ax.legend(title="Simulation Scenarios")
    plt.tight_layout()
    plt.show()


def capacity_tradeoff_plot(all_util_rates: dict, all_travel_times: dict):
    """
    Creates a plot showing the tradeoff between system utilization and travel time.

    For each capacity level provided, this function calculates the average emptyness
    rate (the inverserse of the utilization) and the average travel time.
    It then plots these points on a 2D graph and connects
    them with a line to visualize the tradeoff curve. Lower capacity typically leads to
    higher utilization but also higher travel times, and this plot makes that
    relationship clear.

    Args:
        all_util_rates (dict): A dictionary where keys are integer capacity values
                               and values are lists of utilization rates.
                               Example: {10: [0.95, 0.96], 20: [0.75, 0.76]}

        all_travel_times (dict): A dictionary with matching integer capacity keys
                                 and values that are lists of travel times.
                                 Example: {10: [35, 40], 20: [18, 19]}
    """

    # It's good practice to sort the capacities to ensure the plot line is drawn
    # in a logical and ascending order of capacity.
    if not all_util_rates or not all_travel_times:
        print("Input dictionaries cannot be empty.")
        return

    # I changed this so its the inverse -> now its a minimzation problem
    inverse_util_rates = {}
    for capacity in all_util_rates:
        inverse_util_rates[capacity] = [1 - r for r in all_util_rates[capacity]]

    sorted_capacities = sorted(inverse_util_rates.keys())

    # Calculate the average for each capacity using list comprehensions
    avg_util_rates = [np.mean(inverse_util_rates[cap]) for cap in sorted_capacities]
    avg_travel_times = [np.mean(all_travel_times[cap]) for cap in sorted_capacities]

    ## Create the Plot
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.figure(figsize=(10, 6))

    # Plot the curve connecting the points
    plt.plot(
        avg_travel_times,
        avg_util_rates,
        marker="o",
        linestyle="-",
        color="#007ACC",
        label="Tradeoff Curve",
    )

    # Annotate each point with its capacity value for better readability
    for i, capacity in enumerate(sorted_capacities):
        plt.annotate(
            f"Capacity = {capacity}",
            (avg_travel_times[i], avg_util_rates[i]),
            textcoords="offset points",
            xytext=(0, 10),  # Offset text slightly above the point
            ha="center",
            fontsize=9,
            color="black",
        )

    ## Formatting and Labels
    plt.title("Capacity Tradeoff: 2 Types of Waste", fontsize=16, fontweight="bold")
    plt.xlabel("Average Passenger Travel Duration in Minutes", fontsize=12)
    plt.ylabel("Average Train Emptyness Rate", fontsize=12)
    plt.legend()
    plt.tight_layout()  # Adjust plot to ensure everything fits
    plt.show()
