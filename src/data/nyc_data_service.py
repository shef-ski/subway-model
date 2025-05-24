import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

import pandas

from src.subway.nyc_subway.nyc_subway_line import NycSubwayLine
from src.subway.subway_station import SubwayStation


class NycDataService:

    META_DATA_FILE_NAME = 'line_metadata.csv'
    ESTIMATES_FILE_NAME = 'direction_estimates.csv'
    TRAIN_ARRIVAL_LOOKUP = 'train_arrival_lookup_table.csv'

    def __init__(self):
        self.lane_data = {}
        self.lane_estimation_sampling = {}
        self.data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/line_outputs'))

    def _line_data_exists(self, name):
        folder_path = os.path.join(self.data_path, name)
        required_files = [NycDataService.ESTIMATES_FILE_NAME, NycDataService.META_DATA_FILE_NAME]

        if not os.path.isdir(folder_path):
            print(f"Folder '{name}' does not exist.")
            return False

        missing_files = [f for f in required_files if not os.path.isfile(os.path.join(folder_path, f))]

        if missing_files:
            print(f"Folder '{name}' is missing the following files: {', '.join(missing_files)}")
            return False

        print(f"Folder '{name}' exists and contains all required files.")
        return True


    def load_nyc_line(self, name: str) -> NycSubwayLine:

        if not self._line_data_exists(name):
            raise ValueError(f"Cannot find data for lane {name}")

        metadata_file_path = self._get_metadata_file_path(name)
        stations = []
        with open(metadata_file_path, newline='') as csvfile:
            reader = list(csv.DictReader(csvfile))

            # Determine first and last sort order
            min_sortorder = min(int(row['sortorder']) for row in reader)
            max_sortorder = max(int(row['sortorder']) for row in reader)

            for row in reader:
                sortorder = int(row['sortorder'])
                is_end = sortorder == min_sortorder or sortorder == max_sortorder
                station = SubwayStation(station_id=sortorder, is_end=is_end)
                stations.append(station)

        metadata_file_path = self._get_direction_estimate_path(name)
        lookup_table = pandas.read_csv(metadata_file_path)
        train_spawns = self.read_train_spawns(name, stations)

        return NycSubwayLine(name, stations, lookup_table, train_spawns)

    def _get_metadata_file_path(self, name) -> str:
        folder_path = os.path.join(self.data_path, name)
        return os.path.join(folder_path, NycDataService.META_DATA_FILE_NAME)

    def _get_direction_estimate_path(self, name) -> str:
        folder_path = os.path.join(self.data_path, name)
        return os.path.join(folder_path, NycDataService.ESTIMATES_FILE_NAME)

    def _get_train_arrival_file(self, name) -> str:
        folder_path = os.path.join(self.data_path, name)
        return os.path.join(folder_path, NycDataService.TRAIN_ARRIVAL_LOOKUP)

    def parse_time(self, time_str: str) -> datetime:
        if time_str.startswith("24:"):
            # Adjust to 00: and add one day
            time_obj = datetime.strptime(time_str.replace("24:", "00:", 1), "%H:%M:%S")
            return time_obj + timedelta(days=1)
        if time_str.startswith("25:"):
            # Adjust to 00: and add one day
            time_obj = datetime.strptime(time_str.replace("25:", "01:", 1), "%H:%M:%S")
            return time_obj + timedelta(days=1)
        return datetime.strptime(time_str, "%H:%M:%S")

    def read_train_spawns(self, name: str, stations: List[SubwayStation]) -> Dict[Tuple[str, int, int, int], SubwayStation]:
        result = {}

        start_station = min(stations, key=lambda s: s.id)
        end_station = max(stations, key=lambda s: s.id)

        with open(self._get_train_arrival_file(name), newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                weekday = str(row['service_id'].lower())
                direction = int(row['direction'])
                station_id = int(row['station_id'])
                time_str = row['departure_time']
                time_obj = self.parse_time(time_str)

                key = (weekday, time_obj.hour, time_obj.minute, time_obj.second)

                if direction == 1 and station_id == start_station.id:
                    result[key] = start_station
                elif direction == -1 and station_id == end_station.id:
                    result[key] = end_station
        return result



