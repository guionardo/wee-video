"""API Service"""
from typing import Tuple
import datetime

from src.abstractions.repository import RepositoryAbstraction
from src.abstractions.stats_service import StatsServiceAbstraction
from src.abstractions.video_processor import VideoProcessorAbstraction
from src.api.models.get_video_response import GetVideoResponse
from src.api.models.video_status import VideoStatus
from src.api.models.stats_response import StatsResponse
from src.startup.config import Config


class APIService:

    def __init__(self, repository: RepositoryAbstraction,
                 stats_service: StatsServiceAbstraction,
                 video_processor: VideoProcessorAbstraction,
                 config: Config):
        self._repo = repository
        self._stats = stats_service
        self._processor = video_processor
        self._config = config

    def receive_video(self, body: bytes) -> Tuple[str, float, str]:
        """Persists video and returns id, expected processing time and message"""
        if len(body) > self._config.max_file_size:
            return ('', 0, 'FILE SIZE EXCEPT')
        success, video_id = self._repo.save_video(body)
        if success:
            avg_time = self._stats.get_average_process_time(len(body))
            return (video_id, avg_time, 'SAVED')
        return ('', 0, video_id)

    def process_video(self, video_id: str):
        """Process video to extract data"""
        filename = self._repo.get_video_file(video_id)
        if not filename:
            return

        self._processor.process(video_id)

    def get_video_info(self, video_id: str) -> GetVideoResponse:
        """Returns information from video"""
        data, msg = self._repo.get_video_data(video_id)
        if msg:
            return GetVideoResponse(
                video_id=video_id,
                status=VideoStatus(msg)
            )

        return data

    def get_stats(self) -> StatsResponse:
        return StatsResponse(
            total_video_time=datetime.timedelta(
                seconds=self._stats.total_time()),
            total_video_size=self._stats.total_video_size(),
            video_count=self._stats.video_count(),
            average_time_for_byte=self._stats.average_time_for_byte()
        )
