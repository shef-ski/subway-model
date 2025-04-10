from train import Train


class Station:

    def __init__(self,
                 station_id: int,
                 is_end: bool):

        self.id = station_id
        self.is_end = is_end

        # coords for viz?

        self.passengers_waiting = 0

        # A queue for adding new trains to the station if there already is one at the station
        # For now: only stations with is_start_station can spawn new trains
        self.train_queue = []  # use new_train_arriving = self.train_queue.pop(0)

        self.current_train = None

    @property
    def is_start_station(self):
        return self.is_end and self.id == 1

    def add_train(self, train: Train):

        if not self.is_start_station:
            raise TypeError("Only add trains to the start station.")

        if not self.train_queue:
            self.current_train = train

        else:
            self.train_queue.append(train)
