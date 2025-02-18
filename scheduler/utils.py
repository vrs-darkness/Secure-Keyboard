from sqlalchemy.orm import Session
from ._init import Status, Device
import json


async def get_status(db: Session, mobile_id: str, status_code: str):
    data = db.query(Status)
    if mobile_id and data:
        data = data.filter(Status.mobile_id == mobile_id)
    if status_code and data:
        data = data.filter(Status.status_code == status_code)
    data = data.all().__dict__
    data = [item for item in data if item['_sa_instance_state'] is None]
    data = json.loads(json.dumps(data, default=str))
    return data


async def create_status(db: Session, status: Status):
    db.add(status)
    db.commit()
    db.refresh(status)
    return status


async def update_status(db: Session, status: Status):
    db.query(Status).filter(Status.id == status.id).update(status.__dict__)
    db.commit()
    db.refresh(status)
    return status


async def delete_status(db: Session, status: Status):
    db.delete(status)
    db.commit()
    return status


async def create_device(db: Session, device: Device):
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


async def get_device(db: Session, device_id: str):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    return device


async def update_device(db: Session, device: Device):
    db.query(Device).filter(Device.device_id == device.device_id).update(device.__dict__)  # noqa
    db.commit()


async def delete_device(db: Session, device: Device):
    db.delete(device)
    db.commit()
    return device
