from .adapter import Cloud
from .validators import EventBase


class Ypostirizo():
    """YpostiriZO adapter to push data to the cloud.
    initial_data: dict | EventBase Instance
    """

    def __init__(self, initial_data=None):
        self.event = EventBase(**initial_data)

    def _post(self):
        """Posts the self.event to the cloud to create a new event."""
        return Cloud().send(
            payload=self.event.dict(),
            method='POST'
        )
