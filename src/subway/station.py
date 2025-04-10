from src.constants import TrainState
from train import Train


class Station:

    def __init__(self,
                 station_id: int,
                 is_end: bool):
        self.id = station_id
        self.is_end = is_end

        # x and y coords for viz?

        self.passengers_waiting = 0

        # A queue for adding new trains to the station if there already is one at the station
        # For now: only stations with is_start_station can spawn new trains
        self.train_queue = []  # use new = self.train_queue.pop(0)

        self.current_train = None

    @property
    def is_empty(self):
        return self.current_train is None

    @property
    def is_start_station(self):
        return self.is_end and self.id == 1

    def add_train(self, train: Train):
        """A train gets added by going into a FiFo Queue."""

        if not self.is_start_station:
            raise TypeError("Only add trains to the start station.")

        self.train_queue.append(train)

    def deploy_queued_train(self, current_time):
        """Should only be used in """

        self.current_train = self.train_queue.pop(0)

        # todo update train params? probs not, do it in update all func

        self.current_train.status = TrainState.AT_STATION







#  todo perhaps make a FirstStation subclass
