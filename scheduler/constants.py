from enum import Enum


class StatusCode(Enum):
    TRAIN = "TRAIN"
    TEST = "TEST"


MessageCode: dict[StatusCode, str] = {
    StatusCode.TRAIN: "Training Data is required",
    StatusCode.TEST: "Test Data is required"
}
