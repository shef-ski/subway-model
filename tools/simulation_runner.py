from src.simulation import Simulation


class SimulationRunner:
    """Runs a number of simulations and creates outputs."""

    
    outputs: dict

    def __init__(self, ):

        pass


    def run_simulations(self, n_runs: int, duration: int):



        # todo save the outputs in some form to the object
        self.outputs = {}

        pass




# todo move to the class
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

# todo move to the class
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