import numpy as np
from ..utils import get_all_device  # type: ignore
from .._init import get_db  # type: ignore
from ..schema import RandomDevice, SelectionAlgorithm, DeviceInfo  # type: ignore # noqa

SAMPLE_PERCENTAGE = 20 # noqa
NORMAL_STD_DEV = 0.2 # noqa


async def pick_normal_devices() -> RandomDevice:
    """Selects a percentage of devices using a normal distribution."""
    async for session in get_db():
        devices = await get_all_device(session)
    total_devices = len(devices)

    if total_devices == 0:
        print("No devices found")
        return RandomDevice()

    num_to_pick = max(1, int((SAMPLE_PERCENTAGE / 100) * total_devices))  # Ensure at least 1 # noqa

    # Generate normally distributed indices
    mean_index = total_devices / 2  # Center selection in the middle of the dataset # noqa
    std_dev = NORMAL_STD_DEV * total_devices  # Scale std dev based on total count # noqa

    selected_indices = np.random.normal(loc=mean_index, scale=std_dev, size=num_to_pick)  # noqa
    selected_indices = np.clip(selected_indices, 0, total_devices - 1).astype(int)  # Ensure valid indices # noqa

    # Get unique devices from indices
    selected_devices = [devices[i] for i in selected_indices]  # Use set to avoid duplicates # noqa
    random_device = RandomDevice(
        selection_algorithm=SelectionAlgorithm.normal,
        all_device=list(DeviceInfo(**device) for device in devices),
        percentage_selection=SAMPLE_PERCENTAGE,
        random_device=list(DeviceInfo(**device) for device in selected_devices)
    )
    return random_device
