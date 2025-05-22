# compare utilization rates in 5 simulations


import pandas as pd
import matplotlib
matplotlib.use('TkAgg') # not working even with default 'agg'
from matplotlib import pyplot as plt

from src.simulation import Simulation
# from src.subway.abstract_subway_line import AbstractSubwayLine

# from src.data.nyc_data_service import NycDataService
from src.simulation import Simulation
from src.subway.generic_subway.generic_subway_line import GenericSubwayLine
# from src.animation import animate_simulation

def calculate_average_utilization(sim: Simulation, duration: int, capacity:int) -> float:
    total_utilization = 0
    total_trains = 0

    for _ in range(duration):
        sim.step(capacity=capacity)  
        for line in sim.lines:
            for train in line.get_trains():
                total_utilization += train.pct_utilized
                total_trains += 1

    # Avoid division by zero
    if total_trains == 0:
        return 0

    return total_utilization / total_trains

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
        sim = Simulation()
        line = GenericSubwayLine("U4", 7)  # Customize or extend as needed
        sim.add_line(line)

        # Run the simulation and calculate utilization
        avg_utilization = calculate_average_utilization(sim, duration, capacity=capacity)
        average_utilization_rates[i] = avg_utilization

        # Print the result
        print(f"Average utilization in Simulation {i}: {avg_utilization * 100:.2f}%")

    return average_utilization_rates

# Run the simulations with different capacities
capacities= [100, 300, 500, 700]  # Different capacity assumptions
results= {} 
for capacity in capacities:
    results[capacity]=run_simulations(n=10, duration=3600, capacity=capacity)


# Visualize the results
df=pd.DataFrame(results)
df.plot()

# Create a scatter plot
# plt.scatter(df.index, df.values)

plt.title("Utilization rates")
plt.xlabel('Simulations')
plt.ylabel('Utilization rate (ranging from 0 to 1)') 

plt.legend(title='Maximum train capacity'#, loc='upper left'
           ) 
plt.show()
