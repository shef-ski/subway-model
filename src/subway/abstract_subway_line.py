from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from src.subway.passenger import SubwayPassenger
from src.subway.subway_station import SubwayStation
from src.subway.train import Train


class AbstractSubwayLine(ABC):

    def __init__(self, name: str, stations: List[SubwayStation]):
        self.trains = []
        self.train_queue = []  # store trains which are waiting to be deployed
        self.stations = stations
        self.name = name

        self.first_station = self.stations[0]

    def get_lowest_unused_id(self, trains: List[Train]) -> int:
        used_ids = {train.id for train in trains}
        i = 1
        while i in used_ids:
            i += 1
        return i

    def add_train(self, station: SubwayStation, direction: int, is_rotating_train: bool):

        # Create new train and raise counter to ensure unique naming
        new_train = Train(self.get_lowest_unused_id(self.trains), self.stations, direction, is_rotating_train)
        self.trains.append(new_train)

        # Decide whether to queue or to deploy the new train
        if self.train_queue:
            self.train_queue.append(new_train)
        else:
            if self._first_station_is_available():
                new_train.set_current_station(station)
            else:
                self.train_queue.append(new_train)

    def update(self, current_time: datetime):
        """Try to deploy the first queued train, then update all trains and all stations."""

        self.check_for_train_spawns(current_time)
        self.remove_trains_that_reached_end()

        if self.train_queue and self._first_station_is_available():
            deployed_train = self.train_queue.pop(0)
            deployed_train.set_current_station(self.first_station)

        for train in self.trains:
            train.update(current_time, self.stations)

        for station in self.stations:
            arriving_passengers = self.sample_arriving_passengers(station, current_time)
            station.random_psg_arrival(arriving_passengers)

    def _first_station_is_available(self):
        for train in self.trains:
            if train.current_station is self.first_station:
                return False
        return True

    def get_trains(self) -> List[Train]:
        return self.trains

    def get_stations(self) -> List[SubwayStation]:
        return self.stations

    @abstractmethod
    def sample_arriving_passengers(self, station: SubwayStation, current_time: datetime) -> List[SubwayPassenger]:
        pass

    @abstractmethod
    def check_for_train_spawns(self, current_time):
        pass

    def remove_trains_that_reached_end(self):
        self.trains = [train for train in self.trains if not train.has_finished_tour()]
