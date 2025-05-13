from abc import ABC, abstractmethod
from typing import List

from src.subway.passenger import SubwayPassenger
from src.subway.subway_station import SubwayStation
from src.subway.train import Train


class AbstractSubwayLine(ABC):

    def __init__(self, name:str, stations: List[SubwayStation]):
        self.trains = []
        self.train_queue = []  # store trains which are waiting to be deployed
        self.stations = stations
        self.name = name

        self.first_station = self.stations[0]
        # Used to give unique id's to trains
        self.train_id_counter = 1

    def add_train(self):

        # Create new train and raise counter to ensure unique naming
        new_train = Train(self.train_id_counter, self.stations)
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
            arriving_passengers = self.sample_arriving_passengers(station)
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
    def sample_arriving_passengers(self, station: SubwayStation) -> List[SubwayPassenger]:
        pass