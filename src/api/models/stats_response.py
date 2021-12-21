"""Statistics response"""

from pydantic import BaseModel
from datetime import timedelta


class StatsResponse(BaseModel):
    """Statistics response"""
    total_video_time: timedelta
    total_video_size: int
    video_count: int
    average_time_for_byte: float
