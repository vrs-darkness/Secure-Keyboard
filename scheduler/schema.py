from pydantic import BaseModel, Field
from enum import Enum


class CurrenStatus(BaseModel):
    mobile_id: str
    status_code: str
    data_size: int


class DeviceInfo(BaseModel):
    device_id: str
    device_name: str
    token: str


class SelectionAlgorithm(str, Enum):
    random = "random"
    normal = "normal"
    default = "none"


class RandomDevice(BaseModel):
    selection_algorithm: SelectionAlgorithm = Field(default=SelectionAlgorithm.default)  # noqa
    all_device: list[DeviceInfo] = Field(default=[])
    percentage_selection: int = Field(default=0)
    random_device: list[DeviceInfo] = Field(default=[])
