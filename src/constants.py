import enum

# Units in seconds
TRAVEL_TIME_BETWEEN_STATIONS = 70
DWELL_TIME_AT_STATION = 50  # time spent stopped at a station


class TrainState(enum.Enum):
    """For a cleaner representation than using strings."""
    IN_QUEUE = 1
    AT_STATION = 2
    EN_ROUTE = 3

