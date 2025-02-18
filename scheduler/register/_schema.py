from pydantic import BaseModel


class RegisterDevice(BaseModel):
    device_id: str
    device_name: str
    token: str
