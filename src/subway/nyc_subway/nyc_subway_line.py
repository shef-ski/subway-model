import random
from abc import ABC
from typing import List

import pandas as pd

from src.subway.abstract_subway_line import AbstractSubwayLine
from src.subway.generic_subway.generic_subway_line import GenericSubwayLine
from src.subway.passenger import SubwayPassenger
from src.subway.subway_station import SubwayStation


class NycSubwayLine(AbstractSubwayLine, ABC):

    def __init__(self,
                 name: str,
                 stations: List[SubwayStation],
                 arriving_passengers_lookup: pd.DataFrame):
        self.arriving_passengers_lookup = arriving_passengers_lookup
        super().__init__(name, stations)

    def sample_arriving_passengers(self, station: SubwayStation) -> List[SubwayPassenger]:

        # for now hardcoded time: TODO introduce simulation time
        year = 2025
        month = 1
        day_of_week = "Monday"
        hour_of_day = 8

        stations_excluding_self = [s for s in self.stations if s.id != station.id]

        passengers = []
        for other_station in stations_excluding_self:
            estimated_ridership = self.lookup_ridership(year, month, day_of_week, hour_of_day, station.id, other_station.id)

            for i in range(1, round(estimated_ridership) + 1):
                current_index = self.stations.index(station)
                destination_index = self.stations.index(other_station)

                direction = 1 if destination_index > current_index else -1

                passenger = SubwayPassenger(entry_id=station.id, leave_id=other_station.id, direction=direction)
                passengers.append(passenger)

        return passengers

    def lookup_ridership(self, year, month, day_of_week, hour_of_day, origin, destination):
        df = self.arriving_passengers_lookup
        result = df[
            (df["Year"] == year) &
            (df["Month"] == month) &
            (df["day_of_week"] == day_of_week) &
            (df["hour_of_day"] == hour_of_day) &
            (df["origin"] == origin) &
            (df["destination"] == destination)
            ]["estimated_ridership"]
        return result.iloc[0] if not result.empty else 0