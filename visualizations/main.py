import random

from tools.simulation_runner import SimulationRunner
from visualizations.histogram import plot_distributions_from_dict


N_RUNS = 3
DURATION = 3600

seed = 12345
random.seed(seed)


simulation_runner = SimulationRunner()
simulation_runner.run_simulations(N_RUNS, DURATION)

plot_distributions_from_dict(simulation_runner.all_datapoints)


# todo this code should be run by the simulation_runner
# Run the simulations with different capacities
capacities= [100, 300, 500, 700]  # Different capacity assumptions
results= {}
all_datapoints = {}
for capacity in capacities:
    results[capacity], datapoints = run_simulations(n=2, # Number of simulations
                   duration=3600,  # Duration of each simulation in seconds (e.g. 1 hour)
                   capacity=capacity # Maximum train capacity
                   )
    
    if capacity in all_datapoints:
        all_datapoints[capacity] += datapoints
    else:
        all_datapoints[capacity] = datapoints

