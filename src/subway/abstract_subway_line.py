from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict
import random

from src.subway.event.event import Event
from src.subway.delay.delay import Delay
from src.subway.passenger import SubwayPassenger
from src.subway.subway_station import SubwayStation
from src.subway.train import Train


class AbstractSubwayLine(ABC):
    trains: List[Train]
    train_queue: List[Train]

    def __init__(self, name: str, stations: List[SubwayStation], capacity: int):
        self.trains = []
        self.train_queue = []  # store trains which are waiting to be deployed
        self.stations = stations
        self.name = name
        self.capacity = capacity

        self.first_station = self.stations[0]

    def get_lowest_unused_id(self, trains: List[Train]) -> int:
        used_ids = {train.id for train in trains}
        i = 1
        while i in used_ids:
            i += 1
        return i

    def add_train(
        self, station: SubwayStation, direction: int, is_rotating_train: bool
    ):
        # Create new train and raise counter to ensure unique naming
        new_train = Train(
            self.get_lowest_unused_id(self.trains),
            self.stations,
            direction,
            is_rotating_train,
            capacity=self.capacity,
        )

        self.trains.append(new_train)

        # Decide whether to queue or to deploy the new train
        if self.train_queue:
            self.train_queue.append(new_train)
        else:
            if self._first_station_is_available():
                new_train.set_current_station(station)
            else:
                self.train_queue.append(new_train)

    def update(
        self,
        current_time: datetime,
        events: List[Event],
        breaking_times: List[datetime],
        delays: List[Delay],
    ) -> List[float]:
        """Try to deploy the first queued train, then update all trains and all stations.

        Returns the list of all travel times of those passengers who disembarked
        """
        travel_times = []

        self.check_for_train_spawns(current_time)
        self.remove_trains_that_reached_end()

        if breaking_times:
            self._check_if_train_breaks(current_time, breaking_times)

        if self.train_queue and self._first_station_is_available():
            deployed_train = self.train_queue.pop(0)
            deployed_train.set_current_station(self.first_station)

        for train in self.trains:
            travel_times += train.update(current_time, self.get_train_travel_times())

        for station in self.stations:
            arriving_passengers = self.sample_arriving_passengers(
                station, current_time, events
            )
            station.random_psg_arrival(arriving_passengers)

            if delays and delays[0].start_time <= current_time:
                for delay in delays:
                    if delay.nearest_station_id == station.id:
                        if delay.start_time <= current_time < delay.end_time:
                            station.set_delay_up()
                        else:
                            station.clear_delay_up()
        return travel_times

    def _check_if_train_breaks(
        self, current_time: datetime, breaking_times: List[datetime]
    ):
        if current_time >= breaking_times[0]:
            # Select a (pseudo-)random train which breaks
            broken_train = random.choice(self.trains)
            broken_train.is_broken = True
            breaking_times.pop(0)
            print(f"Train with id {broken_train.id} broke!")

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
    def sample_arriving_passengers(
        self, station: SubwayStation, current_time: datetime, events: List[Event]
    ) -> List[SubwayPassenger]:
        pass

    @abstractmethod
    def check_for_train_spawns(self, current_time):
        pass

    @abstractmethod
    def get_train_travel_times(self) -> Dict[SubwayStation, Dict[int, int]]:
        pass

    def remove_trains_that_reached_end(self):
        self.trains = [train for train in self.trains if not train.has_finished_tour()]
