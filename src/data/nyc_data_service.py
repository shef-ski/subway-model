import csv
import os

import pandas

from src.subway.nyc_subway.nyc_subway_line import NycSubwayLine
from src.subway.subway_station import SubwayStation


class NycDataService:

    META_DATA_FILE_NAME = 'line_metadata.csv'
    ESTIMATES_FILE_NAME = 'direction_estimates.csv'

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

        return NycSubwayLine(name, stations, lookup_table)

    def _get_metadata_file_path(self, name) -> str:
        folder_path = os.path.join(self.data_path, name)
        return os.path.join(folder_path, NycDataService.META_DATA_FILE_NAME)

    def _get_direction_estimate_path(self, name) -> str:
        folder_path = os.path.join(self.data_path, name)
        return os.path.join(folder_path, NycDataService.ESTIMATES_FILE_NAME)




