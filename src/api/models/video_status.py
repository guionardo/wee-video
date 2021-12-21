from enum import Enum


class VideoStatus(Enum):
    Received = "RECEIVED"
    Processing = "PROCESSING"
    Processed = "PROCESSED"
    Error = "ERROR"
