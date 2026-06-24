from datetime import timedelta, datetime


class FixedLatencyModel:

    def __init__(self, milliseconds: int=1000):
        self.delay = timedelta(milliseconds=milliseconds)

    def execution_time(
        self,
        submission_time: datetime
    ) -> datetime:

        return submission_time + self.delay