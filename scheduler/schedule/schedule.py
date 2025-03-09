from FastAPI import FastAPI, Depends, JSONResponse  # type: ignore # noqa
from .schema import CurrenStatus  # type: ignore # noqa
from ._init import get_db  # type: ignore # noqa
from sqlalchemy.orm import Session  # type: ignore # noqa
from .utils import get_status, create_status, update_status, delete_status  # type: ignore # noqa
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
