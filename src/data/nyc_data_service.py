import os

from src.subway.abstract_subway_line import AbstractSubwayLine
from src.subway.nyc_subway.nyc_subway_line import NycSubwayLine


class NycDataService:
    def __init__(self):
        self.lane_data = {}
        self.lane_estimation_sampling = {}
        self.data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/line_outputs'))

    def _line_data_exists(self, name):
        folder_path = os.path.join(self.data_path, name)
        required_files = ['direction_estimates.csv', 'line_metadata.csv']

        if not os.path.isdir(folder_path):
            print(f"Folder '{name}' does not exist.")
            return False

        missing_files = [f for f in required_files if not os.path.isfile(os.path.join(folder_path, f))]

        if missing_files:
            print(f"Folder '{name}' is missing the following files: {', '.join(missing_files)}")
            return False

        print(f"Folder '{name}' exists and contains all required files.")
        return True


    def load_nyc_line(self, name: str) -> AbstractSubwayLine:

        if not self._line_data_exists(name):
            raise ValueError(f"Cannot find data for lane {name}")


        return NycSubwayLine(name, [])




