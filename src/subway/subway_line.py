from src.subway.train import Train
from station import Station


class SubwayLine:

    def __init__(self,
                 name: str,
                 n_stations: int):

        self.name = name
        self.n_stations = n_stations

        # Store the stations and trains in a list
        self.stations = []
        self.trains = []

        # Used to give unique id's to trains
        self.train_id_counter = 1

        # Initialize stations
        # The id's go from 1 to n (no limit to n)
        for station_id in range(1, n_stations+1):
            is_end = (station_id == 1 or station_id == n_stations)
            new_station = Station(station_id, is_end)
            self.stations.append(new_station)

    def add_train(self):

        new_train = Train(self.train_id_counter, highest_station_id=self.n_stations)

        self.trains.append(new_train)

        self.stations[0].add_train(new_train)

        # Add the new train to the starting station
        self.train_id_counter += 1  # to ensure unique naming




