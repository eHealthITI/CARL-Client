from typing import Union

from pydantic import BaseModel
from pydantic.types import List, Optional, OptionalInt

from ypostirizoclient.settings import CLOUD_USER as user


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
    homeIdHash: Optional[str]
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
    requestNodeNeighborStatTimeStemp: int
    requestNodeNeighborState: int
    requestNodeNeighborStateTimeStemp: int
    saveLogs: str
    serialNumber: str
    showChildren: str
    smsNotificationID: int
    smsNotificationType: int
    status: Optional[str]
    sunriseHour: str
    sunsetHour: str
    useTemplate: bool
    userDescription: str
    value: Union[Optional[int], Optional[float], Optional[dict]]
    zwaveBuildVersion: str
    zwaveCompany: str
    zwaveInfo: str
    zwaveRegion: str
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
    remoteGatewayId: int
    viewXml: bool
    configXml: bool
    interfaces: List[str]
    properties: DeviceProperties
    actions: dict
    created: int
    modified: int
    sortOrder: int
