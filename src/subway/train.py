import random
from typing import List, Optional

from src.constants import TrainState, DWELL_TIME_AT_STATION, TRAVEL_TIME_BETWEEN_STATIONS
from src.subway.subway_station import SubwayStation
from src.subway.passenger import SubwayPassenger
from src.utils import format_time


class Train:

    capacity = 500  # quick assumption, do more research on train capacity

    def __init__(self,
                 train_id: int, stations_in_line: List[SubwayStation]):

        self.id = train_id
        self.current_station: Optional[SubwayStation] = None

        self.passengers: List[SubwayPassenger] = []

        self.state = TrainState.IN_QUEUE

        # Travel information
        # Direction is either 1 or -1
        # If 1, the station id is increasing, else decreasing to represent the travel direction ('up' vs 'down')
        self.direction = 1

        self.next_station = None
        self.prev_station = None

        self.remaining_destinations: List[SubwayStation] = stations_in_line
        self.stations_in_line = stations_in_line

        # Time information
        self.arrival_time = None  # int (total seconds) - relevant when state == EN_ROUTE
        self.ready_to_depart_at = None  # int (total seconds) - relevant when state == AT_STATION
        self.previous_departure_time = None

    def __repr__(self):
        return f"Train {self.id}"

    def update(self, current_time: int, stations_list: list):

        # Train is currently at a station
        if self.state == TrainState.AT_STATION:
            if self.ready_to_depart_at is None:  # Train just arrived / was deployed
                # todo the dwell time should not be a constant but a r.v.

                self.ready_to_depart_at = current_time + DWELL_TIME_AT_STATION

                self.remaining_destinations = self.remaining_destinations[1:]
                self.next_station = self.remaining_destinations[0]

                # Passengers leave and enter
                self.psg_exchange(self.current_station)

            if current_time >= self.ready_to_depart_at:  # Depart towards the next station
                print(f"{format_time(current_time)} - {self} departing from {self.current_station} "
                      f"towards {self.next_station}")
                self.state = TrainState.EN_ROUTE
                self.arrival_time = current_time + TRAVEL_TIME_BETWEEN_STATIONS

                self.prev_station = self.current_station
                self.current_station = None  # No longer "at" the previous station
                self.previous_departure_time = self.ready_to_depart_at  # for viz
                self.ready_to_depart_at = None  # Clear departure readiness

        # Train is currently traveling to the next station
        if self.state == TrainState.EN_ROUTE:

            if current_time >= self.arrival_time:  # Train arrived at a station
                print(f"{format_time(current_time)} - {self} arrived at {self.next_station}")
                self.current_station = self.next_station
                self.next_station = None
                self.state = TrainState.AT_STATION
                self.arrival_time = None

                # Reverse directions if arrived end station
                if self.current_station.is_end:
                    print(f"{format_time(current_time)} - {self} arrived at end station, reversing direction.")
                    self.direction *=-1
                    if self.direction == -1:
                        self.remaining_destinations = list(reversed(self.stations_in_line))
                    else:
                        self.remaining_destinations = self.stations_in_line

    def psg_exchange(self,
                     station: SubwayStation):

        # --- Disembarking ---
        # current naive assumption: all passengers leaving at one of the remaining stations (flat percentage)
        #n_leaving = round(1 / (n_stations - 1) * self.n_psg)

        self.passengers = [passenger for passenger in self.passengers if passenger.leave_id != station.id]

        # --- Embarking ---
        entering_passengers = station.get_waiting_psg_for_train([station.id for station in self.remaining_destinations])
        if len(self.passengers) + len(entering_passengers) > self.capacity:
            remaining_capacity = self.capacity - len(self.passengers)
            entering_passengers = random.sample(entering_passengers, remaining_capacity)

        station.remove_waiting_passengers(entering_passengers)
        self.passengers = [*self.passengers, *entering_passengers]

    @property
    def pct_utilized(self):
        return len(self.passengers) / self.capacity

    def set_current_station(self, new_station: SubwayStation):
        self.current_station = new_station
        self.state = TrainState.AT_STATION


