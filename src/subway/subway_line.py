from src.subway.station import Station
from src.subway.train import Train


class SubwayLine:

    def __init__(self,
                 name: str,
                 n_stations: int):

        self.name = name  # e.g., U4

        # Store the stations and trains in a list
        self.stations = []
        self.trains = []
        self.train_queue = []  # store trains which are waiting to be deployed

        # Used to give unique id's to trains
        self.train_id_counter = 1

        # Initialize stations
        # The id's go from 1 to n_stations
        for station_id in range(1, n_stations+1):
            is_end = (station_id == 1 or station_id == n_stations)
            new_station = Station(station_id, is_end)
            self.stations.append(new_station)

        self.first_station = self.stations[0]

    def add_train(self):

        # Create new train and raise counter to ensure unique naming
        new_train = Train(self.train_id_counter)
        self.train_id_counter += 1
        self.trains.append(new_train)

        # Decide whether to queue or to deploy the new train
        if self.train_queue:
            self.train_queue.append(new_train)
        else:
            if self._first_station_is_available():
                new_train.set_current_station(self.first_station)
            else:
                self.train_queue.append(new_train)

    def update(self, current_time):
        """Try to deploy the first queued train, then update all trains."""

        if self.train_queue and self._first_station_is_available():
            deployed_train = self.train_queue.pop(0)
            deployed_train.set_current_station(self.first_station)

        for train in self.trains:
            train.update(current_time, self.stations)

    def _first_station_is_available(self):
        for train in self.trains:
            if train.current_station is self.first_station:
                return False
        return True



