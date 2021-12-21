import logging
import tempfile
import unittest

from src.api.repository.file_repository_ import FileRepository
from src.services.stats_service import StatsService
from src.services.video_processor import VideoProcessor


class TestVideoProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.repository_path = tempfile.TemporaryDirectory()
        stats_service = StatsService()
        cls.repository = FileRepository(cls.repository_path.name)

        cls.processor = VideoProcessor(stats_service, cls.repository)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.repository_path.cleanup()
        return super().tearDownClass()

    def test_process(self):
        file_name = 'tests/olha_so.mp4'
        with open(file_name, 'rb') as file:
            body = file.read()
        video_id, _ = self.repository.save_video(body)
        self.assertNotEqual('', video_id)

        with self.assertLogs('src.services.video_processor', level=logging.INFO):
            self.processor.process(video_id)
