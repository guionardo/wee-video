import logging
from threading import Lock

from src.abstractions.stats_service import StatsServiceAbstraction


class StatsService(StatsServiceAbstraction):

    def __init__(self):
        self._lock = Lock()
        self._total_time = 0
        self._total_video_size = 0
        self._events_count = 0
        self._log = logging.getLogger(__name__)
        super().__init__()

    def add_data(self, video_size: int, process_time: float):
        with self._lock:
            self._total_time += process_time
            self._total_video_size += video_size
            self._events_count += 1
            self._log.debug('add_data(%s , %s) -> %s , %s , %s',
                            video_size, process_time,
                            self._total_video_size,
                            self._total_time,
                            self._events_count)

    def get_average_process_time(self, video_size: int) -> float:
        with self._lock:
            avg = 5 if self._total_video_size == 0 \
                else video_size * self._total_time/self._total_video_size
            self._log.debug(
                'get_average_process_time(%s) = %s', video_size, avg)
            return avg

    def total_time(self) -> float:
        return self._total_time

    def total_video_size(self) -> int:
        return self._total_video_size

    def video_count(self) -> int:
        return self._events_count

    def average_time_for_byte(self) -> float:
        return 0 if self._total_video_size == 0 else \
            self._total_time/self._total_video_size
