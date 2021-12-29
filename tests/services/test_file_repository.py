import tempfile
import unittest

from src.api.models.get_video_response import GetVideoResponse
from src.api.models.video_status import VideoStatus
from src.services.file_repository import FileRepository


class TestFileRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.folder = cls.temp.name
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()
        return super().tearDownClass()

    def test_save_and_load_video(self):
        repo = FileRepository(self.folder)
        data = b'ABCDEFGHIJ'

        success, video_id = repo.save_video(data)
        self.assertTrue(success)

        body, message = repo.get_video_body(video_id)
        self.assertEqual(0, len(message))
        self.assertEqual(data, body)

        video_info = GetVideoResponse(
            video_id=video_id,
            status=VideoStatus.Received,
            processing_time=0.1)

        success, message = repo.update_video(
            video_id, video_info)
        self.assertTrue(success)
        body, message = repo.get_video_body(video_id)
        self.assertEqual(b'', body)

        video_data, message = repo.get_video_data(video_id)
        self.assertEqual(0, len(message))
        self.assertEqual(video_id, video_data.video_id)
