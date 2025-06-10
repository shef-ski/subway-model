from typing import List

from src.subway.passenger import SubwayPassenger


class SubwayStation:

    def __init__(self,
                 station_id: int,
                 is_end: bool,
                 name: str = "",
                 lon: float | None = None,
                 lat: float | None = None):
        self.id = station_id
        self.is_end = is_end

        self.waiting_passengers: List[SubwayPassenger] = []
        self.incoming_train_up = False
        self.incoming_train_down = False
        self.delay_up = False
        self.delay_down = False
        self.name = name
        self.lon = lon
        self.lat = lat

    def __repr__(self):
        return f"Station {self.id}"

    def random_psg_arrival(self, arriving_passengers: List[SubwayPassenger]):
        self.waiting_passengers = [*self.waiting_passengers, *arriving_passengers]

    def get_waiting_psg_for_train(self, remaining_stations_for_train: List[int]) -> List[SubwayPassenger]:
        return [passenger for passenger in self.waiting_passengers if passenger.leave_id in remaining_stations_for_train]

    def remove_waiting_passengers(self, passengers_entering_train: List[SubwayPassenger]):
        self.waiting_passengers = [passenger for passenger in self.waiting_passengers if passenger not in passengers_entering_train]

    def get_waiting_psg_up(self) -> List[SubwayPassenger]:
        return [passenger for passenger in self.waiting_passengers if passenger.direction == 1]

    def get_waiting_psg_down(self) -> List[SubwayPassenger]:
        return [passenger for passenger in self.waiting_passengers if passenger.direction == -1]

    def get_waiting_psg_up_regular(self) -> List[SubwayPassenger]:
        return [passenger for passenger in self.waiting_passengers if passenger.direction == 1 and passenger.event_name is None]

    def get_waiting_psg_down_regular(self) -> List[SubwayPassenger]:
        return [passenger for passenger in self.waiting_passengers if passenger.direction == -1 and passenger.event_name is None]

    def get_waiting_psg_up_event(self) -> List[SubwayPassenger]:
        return [passenger for passenger in self.waiting_passengers if passenger.direction == 1 and passenger.event_name is not None]

    def get_waiting_psg_down_event(self) -> List[SubwayPassenger]:
        return [passenger for passenger in self.waiting_passengers if passenger.direction == -1 and passenger.event_name is not None]

    def get_occupation_up(self):
        return self.incoming_train_up
    def train_incoming_up(self):
        self.incoming_train_up = True
    def train_leave_up(self):
        self.incoming_train_up = False
    def get_occupation_down(self):
        return self.incoming_train_down
    def train_incoming_down(self):
        self.incoming_train_down = True
    def train_leave_down(self):
        self.incoming_train_down = False
    def set_delay_up(self):
        self.delay_up = True
    def set_delay_down(self):
        self.delay_down = True
    def clear_delay_up(self):
        self.delay_up = False
    def clear_delay_down(self):
        self.delay_down = False

    def get_delay_up(self):
        return self.delay_up
    def get_delay_down(self):
        return self.delay_down



