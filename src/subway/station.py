

class Station:

    def __init__(self,
                 station_id: int,
                 is_end: bool):
        self.id = station_id
        self.is_end = is_end

        self.passengers_waiting = 0


