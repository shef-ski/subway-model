from datetime import datetime, timedelta
import pandas as pd
import json
import os
from pathlib import Path

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

    description: str  # needed for plotting

    def __init__(
        self,
        n_runs: int,
        duration: int,
        capacities: list,
        start_time: datetime,
        time_delta: timedelta,
        line_name: str,
    ):
        self.n_runs = n_runs
        self.duration = duration
        self.capacities = capacities
        self.start_time = start_time
        self.time_delta = time_delta
        self.line_name = line_name

        self.average_util_rates = {}
        self.all_util_rates = {}
        self.all_travel_times = {}

        self.breaking_times = []
        self.events = []
        self.delays = []

    def run_simulations(
        self, list_breaking_times: list, list_events: list, list_delays: list
    ):
        print(
            f"\nRunning {self.n_runs * len(self.capacities)} simulations each with {self.duration} seconds."
        )
        if list_breaking_times:
            print(f"Breaking times: {list_breaking_times}")
        if list_events:
            print(f"Events at: {[e.start_time for e in list_events]}")

        for capacity in self.capacities:
            average_utilization_rates = {}

            for run_idx in range(1, self.n_runs + 1):
                print(
                    f"\nSimulation for capacity {capacity}, run number {run_idx}/{self.n_runs}."
                )

                # Create a NYC simulation and a line
                sim = Simulation(self.start_time, self.time_delta)
                nyc_data_service = NycDataService()
                line = nyc_data_service.load_nyc_line(self.line_name, capacity)
                sim.add_line(line)

                if list_breaking_times:
                    sim.add_breaking_times(list_breaking_times)
                    self.breaking_times = list_breaking_times
                if list_events:
                    sim.add_events(list_events)
                    self.events = list_events
                if list_delays:
                    sim.add_delays(list_delays)
                    self.delays = list_delays

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

    def save_outputs(self, base_path: str):
        """
        Saves simulation parameters and results to a new, timestamped directory.

        Args:
            base_path (str): The root directory where the output folder will be created.
        """

        indicator_1 = "T" if self.breaking_times else "F"
        indicator_2 = "T" if self.events else "F"
        indicator_3 = "T" if self.delays else "F"

        # Create a unique directory name for this run to avoid overwriting results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = (
            Path(base_path) / f"sim_{indicator_1}{indicator_2}{indicator_3}_{timestamp}"
        )

        # Create the directory, including any parent directories if they don't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Saving outputs to: {output_dir}")

        # 1. Save simulation metadata (parameters)
        # Convert datetime/timedelta to strings/numbers for JSON compatibility
        metadata = {
            "n_runs": self.n_runs,
            "duration": self.duration,
            "capacities": self.capacities,
            "start_time": self.start_time.isoformat(),
            "time_delta_seconds": self.time_delta.total_seconds(),
            "line_name": self.line_name,
            #            "breaking_times": self.breaking_times,
            #           "events": self.events,
            #            "delays": self.delays
        }
        with open(output_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)

        # 2. Save the result dictionaries
        data_to_save = {
            "average_util_rates": self.average_util_rates,
            "all_util_rates": self.all_util_rates,
            "all_travel_times": self.all_travel_times,
        }

        for filename, data in data_to_save.items():
            with open(output_dir / f"{filename}.json", "w") as f:
                # The keys in your dicts are integers (capacities). JSON keys must
                # be strings, but json.dump handles this conversion automatically.
                json.dump(data, f, indent=4)

        print("Save complete.")

    def load_outputs(self, path: str):
        """
        Loads simulation results from a specified directory into the current instance.

        Note: This method assumes the instance has already been initialized.
        It only loads the data, not the metadata. For a complete load,
        use the `from_saved` classmethod.

        Args:
            path (str): The specific simulation directory containing the .json files.
        """
        load_path = Path(path)
        if not load_path.is_dir():
            raise FileNotFoundError(f"Directory not found: {load_path}")

        print(f"Loading outputs from: {load_path}")

        data_files = {
            "average_util_rates": "average_util_rates.json",
            "all_util_rates": "all_util_rates.json",
            "all_travel_times": "all_travel_times.json",
        }

        for attr_name, filename in data_files.items():
            file_path = load_path / filename
            if file_path.exists():
                with open(file_path, "r") as f:
                    # json.load automatically converts string keys back to numbers if they look like numbers
                    # but it's best practice to handle this explicitly if needed.
                    # Here, we convert keys back to integers for consistency.
                    data = json.load(f)
                    # Convert string keys back to integers for capacities
                    corrected_data = {int(k): v for k, v in data.items()}
                    setattr(self, attr_name, corrected_data)
            else:
                print(f"Warning: Data file not found, skipping: {filename}")

        print("Load complete.")

    @classmethod
    def from_saved(cls, base_path: str, sim_path: str):
        """
        Creates a new SimulationRunner instance by loading metadata and results
        from a specified directory.

        Args:
            path (str): The specific simulation directory to load from.

        Returns:
            SimulationRunner: A new instance populated with the saved data.
        """
        load_path = Path(base_path + sim_path)
        metadata_path = load_path / "metadata.json"

        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found in: {load_path}")

        # 1. Load metadata to initialize the class
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        # Reconstruct the class instance
        instance = cls(
            n_runs=metadata["n_runs"],
            duration=metadata["duration"],
            capacities=metadata["capacities"],
            start_time=datetime.fromisoformat(metadata["start_time"]),
            time_delta=timedelta(seconds=metadata["time_delta_seconds"]),
            line_name=metadata["line_name"],
        )

        # 2. Use the instance method to load the actual result data
        instance.load_outputs(load_path)

        description = sim_path[0:7]
        instance.description = description

        return instance

    @property
    def df_avg_util_rates(self):
        if not self.average_util_rates:
            raise ValueError("No simulations have been run.")

        return pd.DataFrame(self.average_util_rates)
