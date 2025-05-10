import random
from abc import ABC
from typing import List

from src.subway.abstract_station import AbstractStation
from src.subway.abstract_subway_line import AbstractSubwayLine
from src.subway.generic_subway.generic_station import GenericStation
from src.subway.passenger import SubwayPassenger
from src.subway.train import Train


class SubwayLine(AbstractSubwayLine, ABC):

    def __init__(self,
                 name: str,
                 n_stations: int):

        self.name = name  # e.g., U4

        # Store the stations and trains in a list
        self.stations: List[AbstractStation] = []
        self.trains = []
        self.train_queue = []  # store trains which are waiting to be deployed

        # Used to give unique id's to trains
        self.train_id_counter = 1

        # Initialize stations
        # The id's go from 1 to n_stations
        for station_id in range(1, n_stations+1):
            is_end = (station_id == 1 or station_id == n_stations)
            new_station = GenericStation(station_id, is_end)
            self.stations.append(new_station)

        self.first_station = self.stations[0]

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
            arriving_pasengers = self.sample_arriving_passengers(station)
            station.random_psg_arrival(arriving_pasengers)

    def _first_station_is_available(self):
        for train in self.trains:
            if train.current_station is self.first_station:
                return False
        return True


    def get_trains(self) -> List[Train]:
        return self.trains

    def get_stations(self) -> List[AbstractStation]:
        return self.stations

    def sample_arriving_passengers(self, station: AbstractStation) -> List[SubwayPassenger]:
        passengers = []

        if random.random() < AbstractStation.p_arrival_in_a_second:
            # A passenger arrives
            valid_stations = [s for s in self.stations if s.id != station.id]
            destination_station = random.choice(valid_stations)
            current_index = self.stations.index(station)
            destination_index = self.stations.index(destination_station)
            direction = 1 if destination_index > current_index else -1

            passenger = SubwayPassenger(entry_id=station.id, leave_id=destination_station.id, direction=direction)
            passengers.append(passenger)

        return passengers

