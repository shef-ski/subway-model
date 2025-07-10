from datetime import datetime


class Event:
    def __init__(
        self,
        name: str,
        nearest_station_id: int,
        expected_ridership: int,
        start_time: datetime,
        end_time: datetime,
    ):
        self.name = name
        self.nearest_station_id = nearest_station_id
        self.expected_ridership = expected_ridership
        self.start_time = start_time
        self.end_time = end_time
