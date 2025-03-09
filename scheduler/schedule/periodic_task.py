import logging
from .random_picker import pick_normal_devices
from ..schema import RandomDevice, SelectionAlgorithm
from datetime import datetime
from ..notifier.notifier import send_batch_notification
import asyncio
logger = logging.getLogger(__name__)


async def periodic_task():
    # TODO: Add a check to see if the device is online
    # TODO: Add a check to see if the device is offline
    # TODO: To make this API call, we need to get the device id and token from the database # noqa
    logger.info("Periodic task executed.")
    logger.info(f"start time: {datetime.now()}")
    try:
        # Get all random devices from the database
        devices: RandomDevice = await pick_normal_devices()  # type: ignore
        if devices.selection_algorithm == SelectionAlgorithm.default:
            logger.info("No devices found")
            logger.info(f"End of Periodic Task @ {datetime.now()}")
            return
        logger.info(f"No of Live Devices : {len(devices.all_device)}")
        logger.info(f"No of selected Device: {len(devices.random_device)}")
        logger.info(f"Percentage of selection: {devices.percentage_selection}")
        mobile_ids = [device.device_id for device in devices.all_device]
        mobile_tokens = [device.token for device in devices.random_device]
        await send_batch_notification(mobile_ids, mobile_tokens)
        logger.info(f"Notification sent to {len(mobile_tokens)} devices")

        logger.info(f"Selection Algorithm: {devices.selection_algorithm}")
        logger.info(f"End of Periodic Task @ {datetime.now()}")
    except Exception as e:
        logger.error(f"Error in periodic task: {e}")
        logger.info(f"End of Periodic Task @ {datetime.now()}")

if __name__ == "__main__":
    asyncio.run(periodic_task())
