from pydantic import BaseModel


class Event(BaseModel):
    id: int
    user: int
    event_type: str
    type: str
    timestamp: int
    deviceID: int
    deviceType: str
    propertyName: str
    oldValue: int
    newValue: int
