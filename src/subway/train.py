import typing

from src.constants import TrainState, DWELL_TIME_AT_STATION, TRAVEL_TIME_BETWEEN_STATIONS
from src.subway.station import Station
from utils import to_min_sec


class Train:

    capacity = 500  # quick assumption, do more research on train capacity

    def __init__(self,
                 train_id: int):

        self.id = train_id
        self.current_station: typing.Optional[Station] = None

        self.n_passengers = 42  # should be dynamic

        self.state = TrainState.IN_QUEUE

        # Travel information
        # Direction is either 1 or -1
        # If 1, the station id is increasing, else decreasing to represent the travel direction ('up' vs 'down')
        self.direction = 1
        self.next_station = None
        self.prev_station = None

        # Time information
        self.arrival_time = None  # int (total seconds) - relevant when state == EN_ROUTE
        self.ready_to_depart_at = None  # int (total seconds) - relevant when state == AT_STATION
        self.previous_departure_time = None

    def __repr__(self):
        return f"Train {self.id}"

    def update(self, current_time: int, stations_list: list):
        # Train is currently queued and waiting to be deployed
        if self.state == TrainState.IN_QUEUE:
            return  # do nothing

        # Train is currently at a station
        if self.state == TrainState.AT_STATION:
            if self.ready_to_depart_at is None:  # Train just arrived / was deployed
                # todo the dwell time should not be a constant but a r.v.
                # todo passenger exchange

                self.ready_to_depart_at = current_time + DWELL_TIME_AT_STATION

                self.next_station = self._get_next_station(stations_list)

            if current_time >= self.ready_to_depart_at:  # Depart towards the next station
                print(f"{to_min_sec(current_time)} - T{self.id} departing from S{self.current_station.id} "
                      f"towards S{self.next_station.id}")
                self.state = TrainState.EN_ROUTE
                self.arrival_time = current_time + TRAVEL_TIME_BETWEEN_STATIONS

                self.prev_station = self.current_station
                self.current_station = None  # No longer "at" the previous station

                self.previous_departure_time = self.ready_to_depart_at  # for viz

                self.ready_to_depart_at = None  # Clear departure readiness

        # Train is currently traveling to the next station
        if self.state == TrainState.EN_ROUTE:

            if current_time >= self.arrival_time:  # Train arrived at a station
                print(f"{to_min_sec(current_time)} - T{self.id} arrived at S{self.next_station.id}")
                self.current_station = self.next_station
                self.next_station = None
                self.state = TrainState.AT_STATION
                self.arrival_time = None

                # Reverse directions if arrived end station
                if self.current_station.is_end:
                    print(f"{to_min_sec(current_time)} - T{self.id} arrived at end station, reversing direction.")
                    self.direction *= -1

    def _get_next_station(self, stations_list: list):
        current_station_index = self.current_station.id - 1
        return stations_list[current_station_index + self.direction]

    @property
    def pct_utilized(self):
        return self.n_passengers / self.capacity

    def passenger_exchange(self,
                           n_stations: int,
                           n_trying_to_enter: int):

        # disembarking
        # current assumption: all passengers leaving at one of the remaining stations
        n_leaving = round(1/(n_stations - 1) * self.n_passengers)
        self.n_passengers -= n_leaving

        # embarking
        n_entering = 100  # todo this should be function input, based on real data
        if self.n_passengers + n_entering > self.capacity:
            self.n_passengers = self.capacity
            n_entered = self.capacity - self.n_passengers
        else:
            self.n_passengers += n_entering
            n_entered = n_entering

        # return how many people entered the train (useful for
        return n_entered

    def set_station(self, new_station: Station):
        self.current_station = new_station
        self.state = TrainState.AT_STATION


