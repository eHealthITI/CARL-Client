from pydantic import BaseModel


class EventData(BaseModel):
    id: int
    property: str
    oldValue: float
    newValue: float


class Event(BaseModel):
    type: str
    data: EventData


class EventBase(BaseModel):
    id: int
    user: int
    event_type: str
    type: str
    timestamp: int
    deviceID: int
    deviceType: str
    event: Event
