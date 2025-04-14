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

        self.n_psg = 0  # dynamic

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

        # Train is currently at a station
        if self.state == TrainState.AT_STATION:
            if self.ready_to_depart_at is None:  # Train just arrived / was deployed
                # todo the dwell time should not be a constant but a r.v.

                self.ready_to_depart_at = current_time + DWELL_TIME_AT_STATION

                self.next_station = self._get_next_station(stations_list)

                # Passengers leave and enter
                self.psg_exchange(len(stations_list), self.current_station)

            if current_time >= self.ready_to_depart_at:  # Depart towards the next station
                print(f"{to_min_sec(current_time)} - {self} departing from {self.current_station} "
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
                print(f"{to_min_sec(current_time)} - {self} arrived at {self.next_station}")
                self.current_station = self.next_station
                self.next_station = None
                self.state = TrainState.AT_STATION
                self.arrival_time = None

                # Reverse directions if arrived end station
                if self.current_station.is_end:
                    print(f"{to_min_sec(current_time)} - {self} arrived at end station, reversing direction.")
                    self.direction *= -1

    def psg_exchange(self,
                     n_stations: int,
                     station: Station):

        # --- Disembarking ---
        # current naive assumption: all passengers leaving at one of the remaining stations (flat percentage)
        n_leaving = round(1 / (n_stations - 1) * self.n_psg)
        self.n_psg -= n_leaving

        # --- Embarking ---
        n_entering = station.get_waiting_psg(self.direction)
        if self.n_psg + n_entering > self.capacity:
            self.n_psg = self.capacity
            n_entered = self.capacity - self.n_psg
        else:
            self.n_psg += n_entering
            n_entered = n_entering

        station.reduce_waiting_psg(self.direction, n_entered)

    def _get_next_station(self, stations_list: list):
        current_station_index = self.current_station.id - 1
        return stations_list[current_station_index + self.direction]

    @property
    def pct_utilized(self):
        return self.n_psg / self.capacity

    def set_current_station(self, new_station: Station):
        self.current_station = new_station
        self.state = TrainState.AT_STATION


