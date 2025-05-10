from abc import ABC, abstractmethod
from typing import List

from src.subway.station import Station
from src.subway.train import Train


class AbstractSubwayLine(ABC):

    @abstractmethod
    def __init__(self, name: str, n_stations: int):
        """Initialize the subway line with a name and number of stations."""
        pass

    @abstractmethod
    def add_train(self):
        """Add a new train to the subway line."""
        pass

    @abstractmethod
    def update(self, current_time):
        """Update the subway line at the given time."""
        pass

    @abstractmethod
    def _first_station_is_available(self):
        """Check whether the first station is available for a new train."""
        pass

    @abstractmethod
    def get_trains(self) -> List[Train]:
        pass

    @abstractmethod
    def get_stations(self) -> List[Station]:
        pass