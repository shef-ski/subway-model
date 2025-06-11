import random
from datetime import datetime, timedelta
from typing import List, Optional, Dict

from src.constants import TrainState, DWELL_TIME_AT_STATION
from src.subway.subway_station import SubwayStation
from src.subway.passenger import SubwayPassenger
from src.utils import format_time


class Train:

    def __init__(self,
                 train_id: int,
                 stations_in_line: List[SubwayStation],
                 direction: int,
                 is_rotating_train: bool,
                 capacity: int):

        self.capacity = capacity
        self.id = train_id
        self.current_station: Optional[SubwayStation] = None

        self.passengers: List[SubwayPassenger] = []

        self.state = TrainState.IN_QUEUE

        self.direction = direction

        self.next_station = None
        self.prev_station = None

        self.is_rotating_train = is_rotating_train
        self.finished_tour = False

        if direction == 1:
            self.remaining_destinations: List[SubwayStation] = stations_in_line
        else:
            self.remaining_destinations: List[SubwayStation] = stations_in_line[::-1]

        self.stations_in_line = stations_in_line
        self.travel_time_to_next_station = 0

        # Time information
        self.arrival_time = None  # int (total seconds) - relevant when state == EN_ROUTE
        self.ready_to_depart_at = None  # int (total seconds) - relevant when state == AT_STATION
        self.previous_departure_time = None

        self.is_broken = False

    def __repr__(self):
        return f"Train {self.id}"
    
    def update(self,
               current_time: datetime,
               station_travel_times: Dict[SubwayStation, Dict[int, int]]) -> List[float]:
        
        if self.is_broken:
            travel_times = self._update_broken(current_time, station_travel_times)
        else:
            travel_times = self._update_regular(current_time, station_travel_times)

        return travel_times

    def _update_regular(self,
                    current_time: datetime,
                    station_travel_times: Dict[SubwayStation, Dict[int, int]]) -> List[float]:
        travel_times = []

        # Train is currently at a station
        if self.state == TrainState.AT_STATION:
            if self.ready_to_depart_at is None:  # Train just arrived / was deployed

                self.ready_to_depart_at = current_time + timedelta(seconds=max(DWELL_TIME_AT_STATION, round(len(self.current_station.waiting_passengers)/10)))

                self.remaining_destinations = self.remaining_destinations[1:]
                self.next_station = self.remaining_destinations[0]

                # Passengers leave and enter
                travel_times = self._psg_exchange(current_time)

            if current_time >= self.ready_to_depart_at and self.check_station_free() == True:  # Depart towards the next station
                if self.direction == 1:
                    if self.next_station.is_end:
                        self.next_station.train_incoming_down()
                    else:
                        self.next_station.train_incoming_up()
                    self.current_station.train_leave_up()
                else:
                    if self.next_station.is_end:
                        self.next_station.train_incoming_up()
                    else:
                        self.next_station.train_incoming_down()
                    self.current_station.train_leave_down()

                travel_time = station_travel_times[self.next_station][self.direction]

                #print(f"{format_time(current_time)} - {self} departing from {self.current_station} "
                      #f"towards {self.next_station} taking {travel_time} seconds")
                self.state = TrainState.EN_ROUTE
                self.travel_time_to_next_station = travel_time

                self.arrival_time = current_time + timedelta(seconds=travel_time)

                self.prev_station = self.current_station
                self.current_station = None  # No longer "at" the previous station
                self.previous_departure_time = current_time  # for viz
                self.ready_to_depart_at = None  # Clear departure readiness

        # Train is currently traveling to the next station
        if self.state == TrainState.EN_ROUTE:

            if current_time >= self.arrival_time:  # Train arrived at a station
                #print(f"{format_time(current_time)} - {self} arrived at {self.next_station}")
                self.current_station = self.next_station
                self.next_station = None
                self.state = TrainState.AT_STATION
                self.arrival_time = None

                # Reverse directions if rotating train
                if self.current_station.is_end and self.is_rotating_train:
                    #print(f"{format_time(current_time)} - {self} arrived at end station, reversing direction.")
                    self.direction *=-1
                    if self.direction == -1:
                        self.remaining_destinations = list(reversed(self.stations_in_line))
                    else:
                        self.remaining_destinations = self.stations_in_line
                elif self.current_station.is_end:
                    # Non rotating train -> Tour finished
                    self.finished_tour = True

        return travel_times
    
    def _update_broken(self,
                        current_time: datetime,
                        station_travel_times: Dict[SubwayStation, Dict[int, int]]) -> None:
        travel_times = []
        
        if self.state == TrainState.AT_STATION:
            if self.passengers:
                travel_times = self._disembark_all(current_time)
                self.ready_to_depart_at = current_time + timedelta(seconds=DWELL_TIME_AT_STATION)
            else:
                self.ready_to_depart_at = current_time
            self.remaining_destinations = self.remaining_destinations[1:]
            self.next_station = self.remaining_destinations[0]
            if current_time >= self.ready_to_depart_at and self.check_station_free() == True:  # Depart towards the next station
                if self.direction == 1:
                    if self.next_station.is_end:
                        self.next_station.train_incoming_down()
                    else:
                        self.next_station.train_incoming_up()
                    self.current_station.train_leave_up()
                else:
                    if self.next_station.is_end:
                        self.next_station.train_incoming_up()
                    else:
                        self.next_station.train_incoming_down()
                    self.current_station.train_leave_down()

                travel_time = station_travel_times[self.next_station][self.direction]

                #print(f"{format_time(current_time)} - {self} departing from {self.current_station} "
                      #f"towards {self.next_station} taking {travel_time} seconds")
                self.state = TrainState.EN_ROUTE
                self.travel_time_to_next_station = travel_time

                self.arrival_time = current_time + timedelta(seconds=travel_time)

                self.prev_station = self.current_station
                self.current_station = None  # No longer "at" the previous station
                self.previous_departure_time = self.ready_to_depart_at  # for viz
                self.ready_to_depart_at = None  # Clear departure readiness

                # Train is currently traveling to the next station
        if self.state == TrainState.EN_ROUTE:

            if current_time >= self.arrival_time:  # Train arrived at a station
                #print(f"{format_time(current_time)} - {self} arrived at {self.next_station}")
                self.current_station = self.next_station
                self.next_station = None
                self.state = TrainState.AT_STATION
                self.arrival_time = None

                # Reverse directions if rotating train
                if self.current_station.is_end and self.is_rotating_train:
                    #print(f"{format_time(current_time)} - {self} arrived at end station, reversing direction.")
                    self.direction *=-1
                    if self.direction == -1:
                        self.remaining_destinations = list(reversed(self.stations_in_line))
                    else:
                        self.remaining_destinations = self.stations_in_line
                elif self.current_station.is_end:
                    # Non rotating train -> Tour finished
                    self.finished_tour = True

        return travel_times

    def _psg_exchange(self, current_time: datetime) -> List[float]:

        # --- Disembarking ---
        travel_times = self._disembark_arriving_passengers(current_time)

        # --- Embarking ---
        entering_passengers = self.current_station.get_waiting_psg_for_train([station.id for station in self.remaining_destinations])
        if len(self.passengers) + len(entering_passengers) > self.capacity:
            remaining_capacity = self.capacity - len(self.passengers)
            entering_passengers = random.sample(entering_passengers, remaining_capacity)

        self.current_station.remove_waiting_passengers(entering_passengers)
        self.passengers = [*self.passengers, *entering_passengers]

        return travel_times

    def _disembark_all(self, current_time: datetime) -> List[float]:
        """Only used to disembark all passengers when train is broken."""
        # First, regular disembark as usual
        travel_times = self._disembark_arriving_passengers(current_time)

        # The remainder gets added as waiting passengers to the current station
        self.current_station.increase_waiting_passengers(self.passengers)

        # Make train empty
        self.passengers = []

        return travel_times

    def _disembark_arriving_passengers(self,
                                       current_time: datetime) -> List[float]:

        # Count all travel times of disembarking passengers
        travel_times = []
        for passenger in self.passengers:
            if passenger.leave_id == self.current_station.id:
                minutes_difference = (current_time - passenger.spawn_time).total_seconds() / 60
                travel_times.append(minutes_difference)

        # Remove all disembarking passengers
        self.passengers = [passenger for passenger in self.passengers
                           if passenger.leave_id != self.current_station.id]

        return travel_times

    @property
    def pct_utilized(self):
        return len(self.passengers) / self.capacity

    def set_current_station(self, new_station: SubwayStation):
        self.current_station = new_station
        self.state = TrainState.AT_STATION

    def check_station_free(self):
        if self.direction == 1:
            return self.next_station.get_occupation_up() == False and self.current_station.get_delay_up() == False
        else:
            return self.next_station.get_occupation_down() == False and self.current_station.get_delay_down() == False

    def has_finished_tour(self):
        return self.finished_tour

    def get_travel_time(self):
        return self.travel_time_to_next_station


