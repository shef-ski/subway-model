import random
from abc import ABC
from typing import List

from src.subway.abstract_subway_line import AbstractSubwayLine
from src.subway.subway_station import SubwayStation
from src.subway.passenger import SubwayPassenger


class GenericSubwayLine(AbstractSubwayLine, ABC):
    p_arrival_in_a_second = 0.1

    def __init__(self,
                 name: str,
                 n_stations: int):
        stations: List[SubwayStation] = []
        for station_id in range(1, n_stations+1):
            is_end = (station_id == 1 or station_id == n_stations)
            new_station = SubwayStation(station_id, is_end)
            stations.append(new_station)

        super().__init__(name, stations)

    def sample_arriving_passengers(self, station: SubwayStation) -> List[SubwayPassenger]:
        passengers = []

        if random.random() < GenericSubwayLine.p_arrival_in_a_second:
            # A passenger arrives
            valid_stations = [s for s in self.stations if s.id != station.id]
            destination_station = random.choice(valid_stations)
            current_index = self.stations.index(station)
            destination_index = self.stations.index(destination_station)
            direction = 1 if destination_index > current_index else -1

            passenger = SubwayPassenger(entry_id=station.id, leave_id=destination_station.id, direction=direction)
            passengers.append(passenger)

        return passengers

