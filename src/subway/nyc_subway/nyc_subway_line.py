from abc import ABC
from typing import List

from src.subway.abstract_subway_line import AbstractSubwayLine
from src.subway.generic_subway.generic_station import AbstractStation
from src.subway.train import Train


class NycSubwayLine(AbstractSubwayLine, ABC):

    def __init__(self,
                 name: str,
                 stations: List[AbstractStation]):

        self.name = name  # e.g., U4

        # Store the stations and trains in a list
        self.stations = []
        self.trains = []
        self.train_queue = []  # store trains which are waiting to be deployed

        # Used to give unique id's to trains
        self.train_id_counter = 1

        self.first_station = self.stations[0]

    def add_train(self):

        # Create new train and raise counter to ensure unique naming
        new_train = Train(self.train_id_counter)
        self.train_id_counter += 1
        self.trains.append(new_train)

        # Decide whether to queue or to deploy the new train
        if self.train_queue:
            self.train_queue.append(new_train)
        else:
            if self._first_station_is_available():
                new_train.set_current_station(self.first_station)
            else:
                self.train_queue.append(new_train)

    def update(self, current_time):
        """Try to deploy the first queued train, then update all trains and all stations."""

        if self.train_queue and self._first_station_is_available():
            deployed_train = self.train_queue.pop(0)
            deployed_train.set_current_station(self.first_station)

        for train in self.trains:
            train.update(current_time, self.stations)

        for station in self.stations:
            station.random_psg_arrival()

    def _first_station_is_available(self):
        for train in self.trains:
            if train.current_station is self.first_station:
                return False
        return True


    def get_trains(self) -> List[Train]:
        return self.trains

    def get_stations(self) -> List[AbstractStation
    ]:
        return self.stations

