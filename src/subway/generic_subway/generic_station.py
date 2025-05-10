from typing import List

from src.subway.abstract_station import AbstractStation
from src.subway.passenger import SubwayPassenger


class GenericStation(AbstractStation):

    p_arrival_in_a_second = 0.1

    def __init__(self,
                 station_id: int,
                 is_end: bool):
        super().__init__(station_id, is_end)
        self.id = station_id
        self.is_end = is_end

        self.waiting_passengers: List[SubwayPassenger] = []

    def __repr__(self):
        return f"Station {self.id}"

    def random_psg_arrival(self, arriving_passengers: List[SubwayPassenger]):
        """Increment the number of passengers waiting at a station using a random number."""

        self.waiting_passengers = [*self.waiting_passengers, *arriving_passengers]

    def get_waiting_psg_for_train(self, remaining_station: List[int]) -> List[SubwayPassenger]:
        print(remaining_station)
        return [passenger for passenger in self.waiting_passengers if passenger.leave_id in remaining_station]

    def remove_waiting_passengers(self, passengers_entering_train: List[SubwayPassenger]):
        self.waiting_passengers = [passenger for passenger in self.waiting_passengers if passenger not in passengers_entering_train]

    def get_waiting_psg_up(self) -> List[SubwayPassenger]:
        return [passenger for passenger in self.waiting_passengers if passenger.direction == 1]

    def get_waiting_psg_down(self) -> List[SubwayPassenger]:
        return [passenger for passenger in self.waiting_passengers if passenger.direction == -1]
