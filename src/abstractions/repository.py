"""Abstract repository"""

from abc import abstractmethod
from typing import Protocol, Tuple, runtime_checkable


@runtime_checkable
class RepositoryAbstraction(Protocol):
    """Video data repository"""

    @abstractmethod
    def save_video(self, body: bytes) -> Tuple[bool, str]:
        """Save video data and returns a unique id"""

    @abstractmethod
    def update_video(self, video_id: str, video_data: dict) -> Tuple[bool, str]:
        """Update video data, returning success, message"""

    @abstractmethod
    def get_video_body(self, video_id: str) -> Tuple[bytes, str]:
        """Get video body by id - returns body and message"""

    @abstractmethod
    def get_video_data(self, video_id: str) -> Tuple[dict, str]:
        """Get video data by id - returns data and message"""

    @abstractmethod
    def get_video_file(self, video_id: str) -> str:
        """Returns video filename or empty string if not exists"""
