from pydantic import BaseModel
from pydantic.types import List, OptionalInt, Optional

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


class DeviceProperties(BaseModel):
    pollingTimeSec: int
    wakeUpTime: int
    zwaveCompany: str
    zwaveInfo: str
    zwaveVersion: str
    alarmLevel: OptionalInt
    alarmType: OptionalInt
    batteryLevel: int
    batteryLowNotification: bool
    categories: List[str]
    configured: bool
    dead: bool
    deadReason: str
    defInterval: int
    deviceControlType: int
    deviceIcon: int
    emailNotificationID: int
    emailNotificationType: int
    endPointId: int
    firmwareUpdate: Optional[dict]
    lastBreached: OptionalInt
    log: str
    logTemp: str
    manufacturer: str
    markAsDead: bool
    maxInterval: int
    minInterval: int
    model: str
    nodeId: int
    parametersTemplate: int
    pendingActions: bool
    productInfo: str
    pushNotificationID: int
    saveLogs: bool
    serialNumber: str
    smsNotificationID: int
    smsNotificationType: int
    stepInterval: int
    tamper: Optional[bool]
    updateVersion: Optional[str]
    useTemplate: bool
    userDescription: str
    value: Optional[int]


class Device(BaseModel):
    id: int
    name: str
    roomID: int
    view: List[dict]
    type: str
    baseType: str
    enabled: bool
    visible: bool
    isPlugin: bool
    parentId: int
    viewXml: bool
    configXml: bool
    interfaces: List[str]
    properties: DeviceProperties
    actions: dict
    created: int
    modified: int
    sortOrder: int
