from .validators import EventBase


class HomeCenter():
    """Fibaro adapter to consume homecenter.
    """

    def __init__(self, initial_data=None):
        self.event = EventBase(**initial_data)

