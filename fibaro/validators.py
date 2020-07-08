from pydantic import BaseModel
from pydantic.types import List, OptionalInt

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
    alarmLevel: int
    alarmType: int
    batteryLevel: int
    batterLowNotification: bool
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
    firmwareUpdate: dict
    lastBreached: OptionalInt
    log: str
    logTemp: str
    manufacturer: str
    markasDead: bool
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
    smsmNotificationType: int
    stepInterval: int
    tamper: bool
    updateVersion: str
    useTemplate: bool
    userDescription: str
    value: bool


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
