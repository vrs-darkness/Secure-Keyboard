from pydantic import BaseModel


class CurrenStatus(BaseModel):
    mobile_id: str
    status_code: str
    data_size: int