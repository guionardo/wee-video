"""Abstract statistics service"""

from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class StatsServiceAbstraction(Protocol):
    """Statistics"""

    @abstractmethod
    def add_data(self, video_size: int, process_time: float):
        """Add video process data"""

    @abstractmethod
    def get_average_process_time(self, video_size: int) -> float:
        """Get average process time"""

    @abstractmethod
    def total_time(self) -> float:
        """Get total videos time in seconds"""

    @abstractmethod
    def total_video_size(self) -> int:
        """Get total videos size in bytes"""

    @abstractmethod
    def video_count(self) -> int:
        """Get processed videos count"""

    @abstractmethod
    def average_time_for_byte(self) -> float:
        """Get average time for processing one byte in seconds"""
