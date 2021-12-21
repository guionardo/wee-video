import os
import shutil
import tempfile
from typing import Tuple, Union
from uuid import uuid1

from src.api.models.get_video_response import GetVideoResponse
from src.api.models.video_categories import VideoCategory
from src.api.models.video_status import VideoStatus
from src.detection.nsfw_detection import extract_video_frames, predict


class FileRepository:

    def __init__(self, folder: str):
        folder = os.path.abspath(folder)
        if not os.path.isdir(folder):
            os.makedirs(folder, exist_ok=True)
        self._folder = folder

    def save_video(self, body: bytes) -> Tuple[str, str]:
        """Save video into temporary folder for processing
        Returns id (null if not accepted), msg of status"""
        if len(body) == 0:
            return None, 'empty body'

        video_id = str(uuid1())
        video_file = os.path.join(self._folder, video_id)
        try:
            with open(video_file, 'wb') as file:
                file.write(body)
            return video_id, 'OK'
        except:
            return None, 'Failed to write video'

    def get_video_body(self, video_id: str) -> bytes:
        video_file = os.path.join(self._folder, video_id)
        if not os.path.isfile(video_file):
            return None
        try:
            with open(video_file, 'rb') as file:
                body = file.read()
            return body
        except:
            return None

    def process_file(self, video_id: str) -> Union[VideoCategory, None]:
        video_file = os.path.join(self._folder, video_id)
        if not os.path.isfile(video_file):
            return None
        try:
            tmp = tempfile.mkdtemp(suffix=video_id)
            frames = extract_video_frames(video_file, 20, tmp)
            prediction = predict(frames)
            shutil.rmtree(tmp)
            category = VideoCategory(**prediction['data'])
            done_file = os.path.join(self._folder, f'{video_id}.status')
            with open(done_file, 'w') as file:
                file.write(category.json())
            os.unlink(video_file)
            return category
        except:
            return None

    def get_video_status(self, video_id: str) -> VideoCategory:
        done_file = os.path.join(self._folder, f'{video_id}.status')
        if os.path.isfile(done_file):
            category = VideoCategory().parse_file(done_file)
            return category

    def get_video_info(self, video_id: str) -> GetVideoResponse:
        done_file = self._get_done_file(video_id)
        if done_file:
            response = GetVideoResponse()
            if response.load(done_file):
                return response

            return GetVideoResponse(video_id=video_id,
                                    status=VideoStatus.Error,
                                    categories=None)
        video_file = self._get_video_file(video_id)
        if not video_file:
            return GetVideoResponse(video_id=video_id,
                                    status=VideoStatus.Error,
                                    categories=None)

        return GetVideoResponse(video_id=video_id,
                                status=VideoStatus.Processing,
                                categories=VideoCategory())

    def get_video_file(self, video_id: str) -> str:
        return self._get_video_file(video_id)

    def _get_done_file(self, video_id: str) -> str:
        """Returns done file name if exists"""
        done_file = os.path.join(self._folder, f'{video_id}.status')
        return done_file if os.path.isfile(done_file) else ''

    def _get_video_file(self, video_id: str) -> str:
        """Returns video file name if exists"""
        video_file = os.path.join(self._folder, video_id)
        return video_file if os.path.isfile(video_file) else ''
