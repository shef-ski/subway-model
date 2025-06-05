# compare utilization rates in 5 simulations

from datetime import timedelta, datetime
import pandas as pd
import matplotlib
matplotlib.use('TkAgg') # not working even with default 'agg'
from matplotlib import pyplot as plt

from src.simulation import Simulation
# from src.subway.abstract_subway_line import AbstractSubwayLine

from src.data.nyc_data_service import NycDataService
from src.simulation import Simulation
from src.subway.generic_subway.generic_subway_line import GenericSubwayLine
# from src.animation import animate_simulation

def calculate_average_utilization(sim: Simulation, duration: int):
    total_utilization = 0
    total_trains = 0

    train_util_datapoints = []

    for _ in range(duration):
        sim.step()  
        for line in sim.lines:
            for train in line.get_trains():
                total_utilization += train.pct_utilized
                total_trains += 1
                train_util_datapoints.append(train.pct_utilized)

    # Avoid division by zero
    if total_trains == 0:
        return 0

    return total_utilization / total_trains, train_util_datapoints

def plot_distributions_from_dict(data_dict, bins=50, title='Distribution from Dictionary', xlabel='Value', ylabel='Frequency'):
    """
    Plots the distribution of float values from a dictionary as histograms.
    The dictionary keys are used as labels.

    Args:
        data_dict (dict): A dictionary where keys are integers (used as labels)
                          and values are lists of float values. Expected to have 4 entries.
        bins (int, optional): The number of bins for the histograms. Defaults to 50.
        title (str, optional): The title of the plot. Defaults to 'Distribution from Dictionary'.
        xlabel (str, optional): The label for the x-axis. Defaults to 'Value'.
        ylabel (str, optional): The label for the y-axis. Defaults to 'Frequency'.
    """
    if not isinstance(data_dict, dict) or len(data_dict) != 4:
        raise ValueError("Input must be a dictionary containing exactly four key-value pairs.")

    # Ensure keys are integers (or can be clearly represented as labels)
    # and values are lists of numbers
    for key, sublist in data_dict.items():
        if not isinstance(key, int):
            print(f"Warning: Key '{key}' is not an integer. It will be converted to string for the label.")
        if not isinstance(sublist, list) or not all(isinstance(item, (int, float)) for item in sublist):
            raise ValueError(f"The value for key '{key}' must be a list of numbers.")

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] # Standard matplotlib colors
    
    plt.figure(figsize=(12, 7)) # Adjust figure size as needed

    # Iterate through dictionary items, using an index for color selection
    for i, (key, sublist_data) in enumerate(data_dict.items()):
        label = str(key) # Use the dictionary key as the label
        plt.hist(sublist_data, bins=bins, color=colors[i % len(colors)], alpha=0.7, label=label, density=True)
        # Using density=True normalizes the histograms.
        # If you want raw counts, set density=False.

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.legend(title="Labels (Keys)", fontsize=12) # Add a title to the legend if desired
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout() # Adjusts plot to ensure everything fits without overlapping
    plt.show()

def run_simulations(n=5, duration=3600, capacity=500):
    """
    Runs `n` simulations of a subway line and calculates average utilization.

    Parameters:
    - n (int): Number of simulations to run.
    - duration (int): Duration of each simulation in seconds.
    - capacity (int): Capacity of the train (used in utilization calculation).

    Returns:
    - dict: A dictionary mapping simulation number to average utilization rate.
    """
    average_utilization_rates = {}

    for i in range(1, n + 1):
        # Create and configure the simulation
        #sim = Simulation()
        #line = GenericSubwayLine("U4", 7)  # Customize or extend as needed
        #sim.add_line(line)

        sim = Simulation(start_time=datetime(2025, 1, 6, 8, 0),
                         time_delta=timedelta(seconds=1))

        # Create a subway line and a corresponding map
        nyc_data_service = NycDataService()
        line = nyc_data_service.load_nyc_line("Lexington Av", capacity)
        sim.add_line(line)


        # Run the simulation and calculate utilization
        avg_utilization, train_util_datapoints = calculate_average_utilization(sim, duration)
        average_utilization_rates[i] = avg_utilization

        # Print the result
        print(f"Average utilization in Simulation {i} with capacity {capacity}: {avg_utilization * 100:.2f}%")

    return average_utilization_rates, train_util_datapoints

# Run the simulations with different capacities
capacities= [100, 300, 500, 700]  # Different capacity assumptions
results= {}
all_datapoints = {}
for capacity in capacities:
    results[capacity], datapoints =run_simulations(n=2, # Number of simulations
                   duration=3600,  # Duration of each simulation in seconds (e.g. 1 hour)
                   capacity=capacity # Maximum train capacity
                   )
    
    if capacity in all_datapoints:
        all_datapoints[capacity] += datapoints
    else:
        all_datapoints[capacity] = datapoints


plot_distributions_from_dict(all_datapoints)


# Create a DataFrame from the results
df=pd.DataFrame(results)

# Visualize the results - simple plot
df.plot()

plt.title("Utilization rates")
plt.xlabel('Simulations')
plt.ylabel('Utilization rate (ranging from 0 to 1)') 

plt.legend(title='Maximum train capacity'#, loc='upper left'
        ) 
plt.show()


# Create a joint plot with distributions
import seaborn as sns
sns.jointplot(df, 
            #   kind="kde"
              )
plt.show()