from pydantic import BaseModel, Field
from ypostirizoclient.settings import CLOUD_USER as user


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
    type: str
    timestamp: int
    deviceID: int
    deviceType: str
    event: Event
    user = user
