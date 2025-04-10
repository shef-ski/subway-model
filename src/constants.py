import enum


TRAVEL_TIME_BETWEEN_STATIONS = 1
DWELL_TIME_AT_STATION = 1  # minutes (time spent stopped at a station)


class TrainState(enum.Enum):
    """Just for a cleaner representation than using strings."""
    AT_STATION = 1
    EN_ROUTE = 2

