from datetime import datetime


class Delay:
    def __init__(self, name: str, nearest_station_id: int, start_time: datetime, end_time: datetime):
        self.name = name
        self.nearest_station_id = nearest_station_id
        self.start_time = start_time
        self.end_time = end_time