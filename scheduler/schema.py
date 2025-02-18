from pydantic import BaseModel


class CurrenStatus(BaseModel):
    mobile_id: str
    status_code: str
    data_size: int


class DeviceInfo(BaseModel):
    device_id: str
    device_name: str
    token: str