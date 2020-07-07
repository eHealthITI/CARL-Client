from .validators import Event
from .adapter import Cloud


class Ypostirizo():

    def __init__(self, initial_data=None):
        self.event = Event(**initial_data)

    def _post(self):
        return Cloud().send(
            payload=self.event.dict(),
            method='POST'
        )
