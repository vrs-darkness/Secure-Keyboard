from FastAPI import FastAPI, Depends, JSONResponse
from .schema import CurrenStatus
from ._init import get_db
from sqlalchemy.orm import Session
from .utils import get_status, create_status, update_status, delete_status
import logging

logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/current_status")
async def current_status(
    filter: CurrenStatus,
    db: Session = Depends(get_db)
):
    try:
        data = await get_status(db, filter.mobile_id, filter.status_code)
        return JSONResponse(content=data)
    except Exception as e:
        logger.error(f"Error in current_status: {e}")
        return JSONResponse(content="Internal Server Error", status_code=500)

