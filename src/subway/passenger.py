from datetime import datetime

class SubwayPassenger: 

    def __init__(self,
                 entry_id: int,
                 leave_id: int,
                 direction: int,
                 spawn_time: datetime,
                 event_name: str | None = None):
        self.entry_id = entry_id
        self.leave_id = leave_id
        self.direction = direction
        self.spawn_time = spawn_time

        self.event_name = event_name
