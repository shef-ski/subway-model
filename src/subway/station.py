import numpy as np


class Station:

    p_arrival_in_a_second = 0.1

    def __init__(self,
                 station_id: int,
                 is_end: bool):
        self.id = station_id
        self.is_end = is_end

        self.psg_waiting_up = 0
        self.psg_waiting_down = 0

    def __repr__(self):
        return f"Station {self.id}"

    def random_psg_arrival(self):
        """Increment the number of passengers waiting at a station using a random number."""

        # Ensure the first and last stations only have passengers waiting in one direction
        if self.is_end and self.id == 1:  # first station
            self.psg_waiting_up += np.random.binomial(1, self.p_arrival_in_a_second)
        elif self.is_end:  # last station
            self.psg_waiting_down += np.random.binomial(1, self.p_arrival_in_a_second)

        # Regular, non-end stations
        else:
            self.psg_waiting_up += np.random.binomial(1, self.p_arrival_in_a_second)
            self.psg_waiting_down += np.random.binomial(1, self.p_arrival_in_a_second)

    def get_waiting_psg(self, direction: int):
        if direction == 1:
            return self.psg_waiting_up
        if direction == -1:
            return self.psg_waiting_down

    def reduce_waiting_psg(self, direction: int, n_entered_train):
        if direction == 1:
            self.psg_waiting_up -= n_entered_train
        if direction == -1:
            self.psg_waiting_down -= n_entered_train
