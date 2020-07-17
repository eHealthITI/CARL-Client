from typing import Union

from pydantic import BaseModel
from pydantic.types import List, Optional, OptionalInt


class EventBase(BaseModel):
    id: int
    type: str
    timestamp: int
    deviceID: int
    deviceType: str
    propertyName: str
    oldValue = int
    newValue = int


class DeviceProperties(BaseModel):
    UIMessageSendTime: OptionalInt
    autoConfig: OptionalInt
    armConfig: Optional[str]
    alarmDelay: Optional[str]
    armError: Optional[str]
    armed: Optional[str]
    alarmExclude: Optional[str]
    alarmTimeTimestamp: Optional[str]
    batteryLevel: Optional[int]
    batteryLowNotification: Optional[str]
    configured: bool
    date: Optional[str]
    dead: bool
    deviceControlType: int
    deviceIcon: int
    disabled: OptionalInt
    emailNotificationID: int
    emailNotificationType: int
    endPoint: Optional[int]
    endPointId: int
    fibaroAlarm: Optional[bool]
    interval: Optional[int]
    homeIdHash: Optional[str]
    lastBreached: Optional[str]
    liliOffCommand: Optional[str]
    liliOnCommand: Optional[str]
    log: str
    logTemp: str
    manufacturer: str
    markAsDead: bool
    model: str
    nodeId: int
    parameters: Optional[list]
    parametersTemplate: int
    pendingActions: Optional[bool]
    pollingDeadDevice: Optional[bool]
    pollingTime: OptionalInt
    pollingTimeNext: OptionalInt
    pollingTimeSec: int
    productInfo: str
    pushNotificationID: int
    pushNotificationType: OptionalInt
    remoteGatewayId: OptionalInt
    requestNodeNeighborStatTimeStemp: Optional[str]
    requestNodeNeighborState: Optional[str]
    requestNodeNeighborStateTimeStemp: Optional[str]
    saveLogs: bool
    serialNumber: str
    showChildren: Optional[str]
    smsNotificationID: int
    smsNotificationType: int
    status: Optional[str]
    sunriseHour: Optional[str]
    sunsetHour: Optional[str]
    useTemplate: bool
    userDescription: str
    value: Union[Optional[str], Optional[float], Optional[dict]]
    wakeUpTime: Optional[int]
    zwaveBuildVersion: Optional[str]
    zwaveCompany: str
    zwaveInfo: str
    zwaveRegion: Optional[str]
    zwaveVersion: str


class Device(BaseModel):
    id: int
    name: str
    roomID: int
    type: str
    baseType: str
    enabled: bool
    visible: bool
    isPlugin: bool
    parentId: int
    remoteGatewayId: Optional[int]
    viewXml: Optional[bool]
    configXml: Optional[bool]
    interfaces: List[str]
    properties: DeviceProperties
    actions: dict
    created: int
    modified: int
    sortOrder: int
