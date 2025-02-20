from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from ._schema import RegisterDevice  # type: ignore
from .._init import get_db, Device  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from ..utils import create_device  # type: ignore
from uuid import uuid4
app = FastAPI()


@app.post("/register-device")
async def register_device(
    register_device: RegisterDevice,
    db: Session = Depends(get_db)
):
    try:

        device = Device(
            device_id=str(uuid4()),
            device_name=register_device.device_name,
            token=register_device.token
        )
        await create_device(db, device)
        response_payload = {"message": "Device registered successfully"}
        return JSONResponse(content=response_payload, status_code=200)
    except Exception as e:
        response_payload = {"message": f"Error registering device: {e}"}
        return JSONResponse(content=response_payload, status_code=500)
