from typing import Union

from pydantic import BaseModel
from pydantic.types import List, Optional, OptionalInt

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
    UIMesageSendTime: OptionalInt
    autoconfig: OptionalInt
    alarmLevel: OptionalInt
    alarmType: OptionalInt
    batteryLevel: OptionalInt
    batteryLowNotification: Optional[bool]
    categories: Optional[List[str]]
    configured: bool
    date: Optional[str]
    dead: bool
    deadReason: Optional[str]
    defInterval: OptionalInt
    deviceControlType: int
    deviceIcon: int
    disabled: OptionalInt
    emailNotificationID: int
    emailNotificationType: int
    endPoint: Optional[int]
    endPointId: int
    firmwareUpdate: Optional[dict]
    lastBreached: OptionalInt
    liliOffCommand: Optional[str]
    liliOnCommand: Optional[str]
    log: str
    logTemp: str
    manufacturer: str
    markAsDead: bool
    maxInterval: OptionalInt
    minInterval: OptionalInt
    model: str
    nodeId: int
    parameters: Optional[list]
    parametersTemplate: int
    pendingActions: Optional[bool]
    pollingDeadDevice: Optional[bool]
    pollingTime: OptionalInt
    pollingNextTime: OptionalInt
    pollingTimeSec: int
    productInfo: str
    pushNotificationID: int
    pushNotificationType: OptionalInt
    remoteGatewayId: OptionalInt
    saveLogs: bool
    serialNumber: str
    smsNotificationID: int
    smsNotificationType: int
    status: Optional[str]
    stepInterval: OptionalInt
    tamper: Optional[bool]
    updateVersion: Optional[str]
    useTemplate: bool
    userDescription: str
    value: Union[Optional[int], Optional[float], Optional[dict]]
    wakeUpTime: OptionalInt
    zwaveCompany: str
    zwaveInfo: str
    zwaveVersion: str


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
