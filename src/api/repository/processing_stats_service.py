import logging
import os

import filelock


class ProcessStatsService:

    def __init__(self, folder: str):
        folder = os.path.abspath(folder)
        if not os.path.isdir(folder):
            os.makedirs(folder, exist_ok=True)
        self._folder = folder
        self._stat_file = os.path.join(folder, '.stat.csv')
        self._lock = filelock.FileLock(self._stat_file)
        self._last_average_time_for_byte = 0

    def register_process_time(self, video_size: int, time_in_seconds: float):
        with self._lock.acquire(timeout=10, poll_intervall=5):
            with open(self._stat_file, 'w+', encoding='ascii') as file:
                file.write(f'{video_size}:{time_in_seconds}\n')

    def consolidate_stats(self):
        if not os.path.isfile(self._stat_file):
            return
        count = 0
        total_video_size = 0
        total_time = 0
        with self._lock(timeout=10, poll_intervall=5):
            try:
                with open(self._stat_file, encoding='ascii') as file:
                    count = 0
                    for line in file.readlines():
                        video_size, time_in_seconds = [
                            float(w) for w in line.split(':', maxsplit=2)]
                        count += 1
                        total_video_size += video_size
                        total_time += time_in_seconds
            except Exception as exc:
                logging.getLogger(__name__).error(
                    'Error reading stats file @ %s - %s', self._stat_file, exc)

        if count < 2:
            return
        self.register_process_time(
            int(total_video_size/count), total_time/count)
        self._last_average_time_for_byte = total_time/total_video_size

    def get_average_time_to_process(self, video_size: int) -> float:
        self.consolidate_stats()
        return self._last_average_time_for_byte * video_size
