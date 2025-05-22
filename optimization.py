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

def calculate_average_utilization(sim: Simulation, duration: int) -> float:
    total_utilization = 0
    total_trains = 0

    for _ in range(duration):
        sim.step(capacity=500
                 )  # Assuming a default train capacity of 500
        for line in sim.lines:
            for train in line.get_trains():
                total_utilization += train.pct_utilized
                total_trains += 1

    # Avoid division by zero
    if total_trains == 0:
        return 0

    return total_utilization / total_trains

n = 5  # Replace with the desired number of simulations

# Dictionary to store average utilization rates
average_utilization_rates = {}

# Run n simulations
for i in range(1, n + 1):
    # Create and configure the simulation
    sim = Simulation()
    line = GenericSubwayLine("U4", 7, #train_capacity=500
                             )  # Replace with a concrete implementation
    sim.add_line(line)

    # Run the simulation for the specified duration
    duration = 3600  # 1 hour
    avg_utilization = calculate_average_utilization(sim, duration)

    # Store the average utilization in the dictionary
    average_utilization_rates[i] = avg_utilization

    # Print the result for the current simulation
    print(f"Average utilization in Simulation {i}: {avg_utilization * 100:.2f}%")


# Compare the results
print("All average utilizations:")
for sim, utilization in average_utilization_rates.items():
    print(f"{sim}: {utilization * 100:.2f}%")

# Find the simulation with the maximum utilization rate
best_simulation = max(average_utilization_rates, key=average_utilization_rates.get)
# print("*** Best Simulation ***")
print(f"**** Simulation {best_simulation} has the maximum utilization rate. ****")


# Visualize the optimal simulation results (and compare with the others)
pd.DataFrame([average_utilization_rates]).T[0].plot()
plt.title("Utilization rates across all simulations")
plt.xlabel('Simulation')
plt.ylabel('Y Average utilization rate') 
plt.axvline(x=best_simulation, color='red', linestyle='--')
plt.show()

# # capacities = [300, 500, 700]  # Different capacity assumptions
# # for capacity in capacities:
# #     sim = Simulation()
# #     line = GenericSubwayLine("U4", 7, train_capacity=capacity)
# #     sim.add_line(line)
# #     avg_utilization = calculate_average_utilization(sim, duration=3600)
# #     print(f"Train capacity {capacity}: Average utilization = {avg_utilization * 100:.2f}%")