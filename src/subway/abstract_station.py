from abc import ABC, abstractmethod
from typing import List

from src.subway.passenger import SubwayPassenger


class AbstractStation(ABC):
    p_arrival_in_a_second = 0.1

    def __init__(self, station_id: int, is_end: bool):
        self.id = station_id
        self.is_end = is_end

    def __repr__(self):
        return f"Station {self.id}"

    @abstractmethod
    def random_psg_arrival(self, arriving_passengers: List[SubwayPassenger]):
        pass

    @abstractmethod
    def get_waiting_psg_for_train(self, remaining_station_ids_of_train: List[int]) -> List[SubwayPassenger]:
        pass

    @abstractmethod
    def get_waiting_psg_up(self) -> List[SubwayPassenger]:
        pass

    @abstractmethod
    def get_waiting_psg_down(self) -> List[SubwayPassenger]:
        pass


    @abstractmethod
    def remove_waiting_passengers(self, leaving_passengers: List[SubwayPassenger]):
        pass