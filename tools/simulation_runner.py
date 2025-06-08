from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from src.data.nyc_data_service import NycDataService
from src.simulation import Simulation


class SimulationRunner:
    """Runs a number of simulations and creates outputs."""

    # nested dict = {capacity1: {run1: val1}, {run2: val2}, capacity2: ...}
    average_util_rates: dict

    # dict = {capacity1: [val1, val2, ...], capacity2: [val1, val2, ...], ...}
    all_util_rates: dict

    # dict = {capacity1: [val1, val2, ...], capacity2: [val1, val2, ...], ...} 
    all_travel_times: dict

    def __init__(self,
                 n_runs: int,
                 duration: int,
                 capacities: list,
                 start_time: datetime,
                 time_delta: timedelta,
                 line_name: str):
        self.n_runs = n_runs
        self.duration = duration
        self.capacities = capacities
        self.start_time = start_time
        self.time_delta = time_delta
        self.line_name = line_name
    

    def run_simulations(self,
                        list_breaking_times: list,
                        list_events: list):
        
        print(f"\nRunning {self.n_runs * len(self.capacities)} simulations each with {self.duration} seconds.")
        if list_breaking_times:
            print(f"Breaking times: {list_breaking_times}")
        if list_events:
            print(f"Events at: {[e.start_time for e in list_events]}")

        self.average_util_rates = {}
        self.all_util_rates = {}
        self.all_travel_times = {}

        for capacity in self.capacities:

            average_utilization_rates = {}

            for run_idx in range(1, self.n_runs + 1):
                print(f"\nSimulation for capacity {capacity}, run number {run_idx}/{self.n_runs}.")

                # Create a NYC simulation and a line
                sim = Simulation(self.start_time, self.time_delta)
                nyc_data_service = NycDataService()
                line = nyc_data_service.load_nyc_line(self.line_name, capacity)
                sim.add_line(line)

                if list_breaking_times:
                    sim.add_breaking_times(list_breaking_times)
                if list_events:
                    sim.add_events(list_events)

                # Add empty data containers
                total_utilization = 0
                total_trains = 0
                all_train_util_vals = []

                # Run the simulation and store data
                for _ in range(self.duration):
                    sim.step()
                    for line in sim.lines:
                        for train in line.get_trains():
                            total_utilization += train.pct_utilized
                            total_trains += 1

                            all_train_util_vals.append(train.pct_utilized)

                # Update the data for average utilization rates in a run
                average_utilization_rates[run_idx] = total_utilization / total_trains

                # Update the data for all utilizations rates (of all runs for the capacity)
                if capacity in self.all_util_rates:
                    self.all_util_rates[capacity] += all_train_util_vals
                else:
                    self.all_util_rates[capacity] = all_train_util_vals

                # Same for passenger travel times
                if capacity in self.all_travel_times:
                    self.all_travel_times[capacity] += sim.all_passenger_travel_times
                else:
                    self.all_travel_times[capacity] = sim.all_passenger_travel_times

            
            self.average_util_rates[capacity] = average_utilization_rates


    def save_outputs_to_csv(self, path):
        # todo

        pass

    @property
    def df_avg_util_rates(self):
        if not self.average_util_rates:
            raise ValueError("No simulations have been run.")

        return pd.DataFrame(self.average_util_rates)

