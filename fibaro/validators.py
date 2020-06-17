from pydantic import BaseModel


class Event(BaseModel):
    id: int
    type: str
    timestamp: int
    deviceID: int
    deviceType: str
    propertyName: str
    oldValue: int
    newValue: int
