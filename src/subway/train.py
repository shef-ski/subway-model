

class Train:

    capacity = 1100  # based on a quick google search

    def __init__(self,
                 train_id: int,
                 highest_station_id: int):

        self.id = train_id
        self.n_passengers = 0

        # A train travels back and forth between the station with highest and lowest id (they are sorted)
        self.current_station_id = 1
        self.highest_station_id = highest_station_id

        # Direction is either 1 or -1
        # If 1, the station id is increasing, else decreasing to represent the travel direction ('up' vs 'down')
        self.direction = 1

    @property
    def pct_utilized(self):
        return self.n_passengers / self.capacity

    def passenger_exchange(self,
                           n_stations: int,
                           n_trying_to_enter: int):

        # disembarking
        # current assumption: all passengers leaving at one of the remaining stations
        n_leaving = round(1/(n_stations - 1) * self.n_passengers)
        self.n_passengers -= n_leaving

        # embarking
        n_entering = 100  # todo this should be function input, based on real data
        if self.n_passengers + n_entering > self.capacity:
            self.n_passengers = self.capacity
            n_entered = self.capacity - self.n_passengers
        else:
            self.n_passengers += n_entering
            n_entered = n_entering

        # return how many people entered the train (useful for
        return n_entered




