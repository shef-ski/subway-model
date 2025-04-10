from src.constants import TrainState, DWELL_TIME_AT_STATION, TRAVEL_TIME_BETWEEN_STATIONS


class Train:

    capacity = 500  # quick assumption, do more research on train capacity

    def __init__(self,
                 train_id: int,
                 highest_station_id: int):
        self.id = train_id

        # A train travels back and forth between the station with highest and lowest id (they are sorted)
        self.current_station_id = 1
        self.highest_station_id = highest_station_id

        self.n_passengers = 0
        self.state = TrainState.IN_QUEUE

        # Direction is either 1 or -1
        # If 1, the station id is increasing, else decreasing to represent the travel direction ('up' vs 'down')
        self.direction = 1

        # Travel information
        self.next_station_id = None  # Update via: self.current_station_id + self.direction

        # Time information
        self.arrival_time = None  # int (total seconds)
        self.ready_to_depart_at = None  # int (total seconds)

    def update(self, current_time):
        # Train is currently queued and waiting to be deployed
        if self.state == TrainState.IN_QUEUE:
            return

        # Train is currently at a station
        if self.state == TrainState.AT_STATION:

            if self.ready_to_depart_at is None:  # in case it just arrived
                self.ready_to_depart_at = current_time + DWELL_TIME_AT_STATION
                self.next_station_id = self.current_station_id + self.direction

            if current_time >= self.ready_to_depart_at:  # Depart towards the next station

                print(f"Minute {current_time/60}: {self.id} departing from {self.current_station_id}"
                      f"towards Station {self.next_station_id}")
                self.state = TrainState.EN_ROUTE
                self.arrival_time = current_time + TRAVEL_TIME_BETWEEN_STATIONS
                self.current_station_id = None  # No longer "at" the previous station
                self.ready_to_depart_at = None  # Clear departure readiness

        # Train is currently traveling to the next station
        if self.state == TrainState.EN_ROUTE:

            if current_time >= self.arrival_time:  # Train arrived at destination
                print(f"Minute {current_time/60}: {self.id} arrived at Station {self.next_station_id}")
                self.current_station_id = self.next_station_id
                self.state = TrainState.AT_STATION
                self.next_station_id = None
                self.arrival_time = None
                self.ready_to_depart_at = current_time + DWELL_TIME_AT_STATION  # Set departure time

                # Check if we need to reverse direction because end station reached
                if self.current_station_id in [1, self.highest_station_id]:
                    print(f"Minute {current_time/60}: {self.id} reached end station, reversing direction.")
                    self.direction *= -1

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




