import matplotlib.pyplot as plt
import numpy as np


def capacity_tradeoff_plot(all_util_rates: dict, all_travel_times: dict):
    """
    Creates a plot showing the tradeoff between system utilization and travel time.

    For each capacity level provided, this function calculates the average utilization rate
    and the average travel time. It then plots these points on a 2D graph and connects
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
        inverse_util_rates[capacity] = [1-r for r in all_util_rates[capacity]]
        
    sorted_capacities = sorted(inverse_util_rates.keys())

    # Calculate the average for each capacity using list comprehensions
    avg_util_rates = [np.mean(inverse_util_rates[cap]) for cap in sorted_capacities]
    avg_travel_times = [np.mean(all_travel_times[cap]) for cap in sorted_capacities]

    ## Create the Plot
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(10, 6))

    # Plot the curve connecting the points
    plt.plot(avg_travel_times, avg_util_rates, marker='o', linestyle='-', color='#007ACC', label='Tradeoff Curve')

    # Annotate each point with its capacity value for better readability
    for i, capacity in enumerate(sorted_capacities):
        plt.annotate(f'Capacity = {capacity}',
                     (avg_travel_times[i], avg_util_rates[i]),
                     textcoords="offset points",
                     xytext=(0, 10),  # Offset text slightly above the point
                     ha='center',
                     fontsize=9,
                     color='black')

    ## Formatting and Labels
    plt.title('Capacity Tradeoff: 2 Types of Waste', fontsize=16, fontweight='bold')
    plt.xlabel('Average Passenger Travel Duration in Minutes', fontsize=12)
    plt.ylabel('Average Train Emptyness Rate', fontsize=12)
    plt.legend()
    plt.tight_layout()  # Adjust plot to ensure everything fits
    plt.show()

