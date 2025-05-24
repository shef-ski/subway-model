import random
from abc import ABC
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

import pandas as pd

from src.subway.abstract_subway_line import AbstractSubwayLine
from src.subway.passenger import SubwayPassenger
from src.subway.subway_station import SubwayStation


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

    def __init__(self,
                 name: str,
                 stations: List[SubwayStation],
                 arriving_passengers_lookup: pd.DataFrame,
                 train_spawns: Dict[Tuple[str, int, int, int], SubwayStation]):
        self.arriving_passengers_lookup = arriving_passengers_lookup
        self.sampled_lookup = {}
        self.train_spawns = train_spawns
        super().__init__(name, stations)

    def sample_arriving_passengers(self, station: SubwayStation, current_time: datetime) -> List[SubwayPassenger]:

        stations_excluding_self = [s for s in self.stations if s.id != station.id]

        passengers = []

        self._clean_old_entries(current_time)
        for other_station in stations_excluding_self:
            estimated_ridership = self.get_arrivals_for_current_time(current_time, station.id, other_station.id)

            for i in range(1, round(estimated_ridership) + 1):
                current_index = self.stations.index(station)
                destination_index = self.stations.index(other_station)

                direction = 1 if destination_index > current_index else -1

                passenger = SubwayPassenger(entry_id=station.id, leave_id=other_station.id, direction=direction)
                passengers.append(passenger)

        return passengers

    def _clean_old_entries(self, now: datetime):
        # Ridership is sampeled at the start of the hour. This removes the dictionary for the old sampled times
        keys_to_delete = [
            key for key in self.sampled_lookup
            if datetime(key[0], key[1], key[2]).replace(hour=key[3]) < now.replace(minute=0, second=0, microsecond=0)
        ]
        for key in keys_to_delete:
            print(f"cleaned entry {key}")
            del self.sampled_lookup[key]

    @staticmethod
    def _lookup_key(dt: datetime, origin, destination):
        return dt.year, dt.month, dt.day, dt.hour , origin, destination

    def lookup_ridership_for_hour(self, current_time: datetime, origin, destination):
        df = self.arriving_passengers_lookup

        year = current_time.year
        month = current_time.month
        day_of_week = current_time.strftime("%A")
        hour_of_day = current_time.hour

        result = df[
            (df["Year"] == year) &
            (df["Month"] == month) &
            (df["day_of_week"] == day_of_week) &
            (df["hour_of_day"] == hour_of_day) &
            (df["origin"] == origin) &
            (df["destination"] == destination)
            ]["estimated_ridership"]
        return result.iloc[0] if not result.empty else 0

    def get_arrivals_for_current_time(self, current_time: datetime, origin, destination):
        # key to lookup sampled arrival times
        key = self._lookup_key(current_time, origin, destination)
        if key not in self.sampled_lookup:
            start_of_hour = current_time.replace(minute=0, second=0, microsecond=0)
            total_people = self.lookup_ridership_for_hour(current_time, origin, destination)
            self.sampled_lookup[key] = self.generate_arrival_times_for_hour(start_of_hour, round(total_people), 0.3)

        return self.sampled_lookup[key].get(current_time, 0)


    def generate_arrival_times_for_hour(self, start_time: datetime, total_people: int, randomness: float = 0.1) -> dict:

        ## Given the total people for this hour we generate randomly distributd arrival timestamps within this hour
        total_seconds = 3600
        if total_people <= 0:
            return {}

        # Special case: very small counts (e.g. 1–3 people)
        if total_people <= 3:
            result = {}
            for _ in range(total_people):
                sec_offset = random.randint(0, total_seconds - 1)
                dt = start_time + timedelta(seconds=sec_offset)
                result[dt] = result.get(dt, 0) + 1
            return result

        base = total_people // total_seconds
        remainder = total_people % total_seconds

        distribution = [base] * total_seconds

        # Distribute remainder randomly
        for _ in range(remainder):
            i = random.randint(0, total_seconds - 1)
            distribution[i] += 1

        # small noise
        swaps = int(total_people * randomness)

        # Find all indices with non-zero counts (candidates to take from)
        nonzero_indices = [i for i, count in enumerate(distribution) if count > 0]

        for _ in range(swaps):
            if not nonzero_indices:
                break

            from_i = random.choice(nonzero_indices)

            # Bias: try to move to a bin that already has people (more likely to create spikes)
            weighted_indices = [i for i, count in enumerate(distribution) if count > 0]
            # fallback if no weighted candidate
            if not weighted_indices:
                to_i = random.randint(0, total_seconds - 1)
            else:
                to_i = random.choice(weighted_indices)

            if distribution[from_i] > 0 and from_i != to_i:
                distribution[from_i] -= 1
                distribution[to_i] += 1

        # Build datetime → count mapping
        datetime_distribution = {
            start_time + timedelta(seconds=i): count
            for i, count in enumerate(distribution)
            if count > 0
        }
        return datetime_distribution



    def check_for_train_spawns(self, current_time: datetime):

        key = build_lookup_key_from_datetime(current_time)

        if key in self.train_spawns:
            print("spawn")
            spawning_station = self.train_spawns[key]
            direction = 1 if spawning_station.id == 0 else -1

            self.add_train(spawning_station, direction, False)