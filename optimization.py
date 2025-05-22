# compare utilization rates in two simulations


from src.simulation import Simulation
from src.subway.abstract_subway_line import AbstractSubwayLine

from src.data.nyc_data_service import NycDataService
from src.simulation import Simulation
from src.subway.generic_subway.generic_subway_line import GenericSubwayLine
from src.animation import animate_simulation

def calculate_average_utilization(sim: Simulation, duration: int) -> float:
    total_utilization = 0
    total_trains = 0

    for _ in range(duration):
        sim.step(#train_capacity=500
                 )  # Assuming a default train capacity of 500
        for line in sim.lines:
            for train in line.get_trains():
                total_utilization += train.pct_utilized
                total_trains += 1

    # Avoid division by zero
    if total_trains == 0:
        return 0

    return total_utilization / total_trains

# Create and configure the first simulation
sim1 = Simulation()
line1 = GenericSubwayLine("U4", 7)  # Replace with a concrete implementation
sim1.add_line(line1)

# Create and configure the second simulation
sim2 = Simulation()
line2 = GenericSubwayLine("U4", 7)  # Replace with a different configuration if needed
sim2.add_line(line2)

# Run both simulations for the same duration
duration = 3600  # 1 hour
avg_utilization_sim1 = calculate_average_utilization(sim1, duration)
avg_utilization_sim2 = calculate_average_utilization(sim2, duration)

# Compare the results
print(f"Average utilization in Simulation 1: {avg_utilization_sim1 * 100:.2f}%")
print(f"Average utilization in Simulation 2: {avg_utilization_sim2 * 100:.2f}%")

if avg_utilization_sim1 > avg_utilization_sim2:
    print("Simulation 1 has better train utilization.")
elif avg_utilization_sim1 < avg_utilization_sim2:
    print("Simulation 2 has better train utilization.")
else:
    print("Both simulations have the same average train utilization.")
