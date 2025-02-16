import asyncio
from .constants import MessageCode, StatusCodes
from firebase_admin import messaging
import logging

logger = logging.getLogger(__name__)


async def send_batch_notification(
        mobile_ids: list[str],
        mobile_tokens: list[str],
        status_code: StatusCodes = StatusCodes.TRAIN
):
    try:
        notifications = [
            messaging.Messages(
                notification=messaging.Notification(
                    title=f"{status_code}",
                    body=MessageCode[status_code]
                ),
                token=mobile_tokens[i]
            ) for i in range(len(mobile_ids))
        ]
        response = await asyncio.to_thread(messaging.send_all, notifications)
        return response
    except Exception as e:
        logger.error(f"Error in sed_notification: {e}")
        return None
