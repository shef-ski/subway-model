import random
from abc import ABC
from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd

from src.subway.abstract_subway_line import AbstractSubwayLine
from src.subway.event.event import Event
from src.subway.passenger import SubwayPassenger
from src.subway.subway_station import SubwayStation


def event_starts_within_next_hour(current_time: datetime, event: Event) -> bool:
    return event.start_time <= current_time + timedelta(hours=1)


def build_lookup_key_from_datetime(current_time: datetime) -> Tuple[str, int, int, int]:
    weekday_index = current_time.weekday()  # Monday = 0, Sunday = 6

    if weekday_index < 5:
        day_type = "weekday"
    elif weekday_index == 5:
        day_type = "saturday"
    else:
        day_type = "sunday"

    return day_type, current_time.hour, current_time.minute, current_time.second


class NycSubwayLine(AbstractSubwayLine, ABC):
    def __init__(
        self,
        name: str,
        stations: List[SubwayStation],
        arriving_passengers_lookup: pd.DataFrame,
        train_spawns: Dict[Tuple[str, int, int, int], SubwayStation],
        train_travel_times: Dict[SubwayStation, Dict[int, int]],
        capacity: int,
    ):
        self.arriving_passengers_lookup = arriving_passengers_lookup
        self.sampled_lookup = {}
        self.sampled_event_lookup = {}
        self.train_spawns = train_spawns
        self.train_travel_times = train_travel_times

        super().__init__(name, stations, capacity)

    def distribute_event_passengers_uniform_dict(self, stations, total_passengers):
        n = len(stations)
        probs = np.ones(n) / n
        passenger_counts = np.random.multinomial(total_passengers, probs)

        return dict(zip(stations, passenger_counts))

    def sample_arriving_passengers(
        self, station: SubwayStation, current_time: datetime, events: List[Event]
    ) -> List[SubwayPassenger]:
        stations_excluding_self = [s for s in self.stations if s.id != station.id]

        passengers = []

        self._clean_old_entries(current_time)
        for other_station in stations_excluding_self:
            estimated_ridership = self.get_arrivals_for_current_time(
                current_time, station.id, other_station.id
            )
            estimated_ridership_event = self.get_arrivals_for_events(
                current_time, station.id, other_station.id, events
            )

            for key, value in estimated_ridership_event.items():
                for i in range(1, value + 1):
                    current_index = self.stations.index(station)
                    destination_index = self.stations.index(other_station)

                    direction = 1 if destination_index > current_index else -1

                    passenger = SubwayPassenger(
                        entry_id=station.id,
                        leave_id=other_station.id,
                        direction=direction,
                        spawn_time=current_time,
                        event_name=key,
                    )
                    passengers.append(passenger)

            for i in range(1, round(estimated_ridership) + 1):
                current_index = self.stations.index(station)
                destination_index = self.stations.index(other_station)

                direction = 1 if destination_index > current_index else -1

                passenger = SubwayPassenger(
                    entry_id=station.id,
                    leave_id=other_station.id,
                    direction=direction,
                    spawn_time=current_time,
                )
                passengers.append(passenger)

        return passengers

    def _clean_old_entries(self, now: datetime):
        # Ridership is sampeled at the start of the hour. This removes the dictionary for the old sampled times
        keys_to_delete = [
            key
            for key in self.sampled_lookup
            if datetime(key[0], key[1], key[2]).replace(hour=key[3])
            < now.replace(minute=0, second=0, microsecond=0)
        ]

        event_keys_to_delete = [
            key
            for key in self.sampled_event_lookup
            if datetime(key[0], key[1], key[2]).replace(hour=key[3])
            < now.replace(minute=0, second=0, microsecond=0)
        ]

        for key in keys_to_delete:
            del self.sampled_lookup[key]

        for key in event_keys_to_delete:
            del self.sampled_event_lookup[key]

    @staticmethod
    def _lookup_key(dt: datetime, origin, destination):
        return dt.year, dt.month, dt.day, dt.hour, origin, destination

    @staticmethod
    def _event_lookup_key(dt: datetime, event_name, origin, destination):
        return dt.year, dt.month, dt.day, dt.hour, event_name, origin, destination

    def lookup_ridership_for_hour(self, current_time: datetime, origin, destination):
        df = self.arriving_passengers_lookup

        year = current_time.year
        month = current_time.month
        day_of_week = current_time.strftime("%A")
        hour_of_day = current_time.hour

        result = df[
            (df["Year"] == year)
            & (df["Month"] == month)
            & (df["day_of_week"] == day_of_week)
            & (df["hour_of_day"] == hour_of_day)
            & (df["origin"] == origin)
            & (df["destination"] == destination)
        ]["estimated_ridership"]
        return result.iloc[0] if not result.empty else 0

    def get_arrivals_for_current_time(
        self, current_time: datetime, origin, destination
    ):
        # key to lookup sampled arrival times
        key = self._lookup_key(current_time, origin, destination)
        if key not in self.sampled_lookup:
            total_people = self.lookup_ridership_for_hour(
                current_time, origin, destination
            )
            self.sampled_lookup[key] = self.generate_arrival_times_for_hour(
                current_time, current_time + timedelta(hours=1), round(total_people)
            )

        return self.sampled_lookup[key].get(current_time, 0)

    def generate_arrival_times_for_hour(
        self, start_time: datetime, end_time: datetime, total_people: int
    ) -> dict:
        if total_people <= 0:
            return {}

        # Compute end of the current hour
        end_of_window = end_time
        remaining_seconds = (end_of_window - start_time).total_seconds()
        lambda_sec = total_people / remaining_seconds

        distribution = defaultdict(int)
        current_time = start_time

        while current_time < end_of_window:
            # Sample time until next event
            delta_seconds = np.random.exponential(scale=1 / lambda_sec)
            current_time += timedelta(seconds=delta_seconds)

            if current_time < end_of_window:
                # Round to the nearest second
                rounded_time = current_time.replace(microsecond=0)
                distribution[rounded_time] += 1

        return dict(distribution)

    def get_train_travel_times(self) -> Dict[SubwayStation, Dict[int, int]]:
        return self.train_travel_times

    def check_for_train_spawns(self, current_time: datetime):
        key = build_lookup_key_from_datetime(current_time)

        if key in self.train_spawns:
            spawning_station = self.train_spawns[key]
            direction = 1 if spawning_station.id == 0 else -1

            self.add_train(spawning_station, direction, False)

    def get_arrivals_for_events(
        self,
        current_time: datetime,
        station_id: int,
        other_station_id: int,
        events: List[Event],
    ) -> Dict[str, int]:
        arrival_dict = {}

        for event in events:
            key = self._event_lookup_key(
                current_time, event.name, station_id, other_station_id
            )
            if key not in self.sampled_event_lookup:
                # Arriving passengers for event
                if (
                    event_starts_within_next_hour(current_time, event)
                    and event.nearest_station_id == other_station_id
                ):
                    total_people = round(event.expected_ridership / len(self.stations))
                    self.sampled_event_lookup[key] = (
                        self.generate_arrival_times_for_hour(
                            current_time, event.start_time, total_people
                        )
                    )

                # Passengers leaving after event
                if (
                    event.nearest_station_id == station_id
                    and event.end_time == current_time
                ):
                    total_people = round(event.expected_ridership / len(self.stations))
                    print(f"adding {total_people} leaving event people for key {key}")
                    self.sampled_event_lookup[key] = (
                        self.generate_arrival_times_for_hour(
                            current_time,
                            current_time + timedelta(hours=1),
                            total_people,
                        )
                    )

            arrival_dict[event.name] = self.sampled_event_lookup.get(key, {}).get(
                current_time, 0
            )

        return arrival_dict
