import glob
import logging
import os
import time
import uuid
from typing import Tuple

from pydantic import BaseModel
from src.abstractions.repository import RepositoryAbstraction
from src.api.models.get_video_response import GetVideoResponse
from src.api.models.video_status import VideoStatus


class FileRepository(RepositoryAbstraction):

    BODY = 'body'
    DATA = 'data'

    def __init__(self, data_folder: str):
        if not os.path.isdir(data_folder):
            raise FileNotFoundError("DATA_FOLDER", data_folder)
        self._folder = os.path.abspath(data_folder)
        self._last_purge = 0
        self._log = logging.getLogger(__name__)
        self._log.info('FileRepository INIT %s', self._folder)

    def save_video(self, body: bytes) -> Tuple[bool, str]:
        """Save video data and returns a unique id"""
        self._purge_old_files()
        video_id = str(uuid.uuid1())
        file_name = self._filename(video_id, self.BODY)
        try:
            with open(file_name, mode='wb') as file:
                file.write(body)
            return (True, video_id)
        except Exception as exc:
            return (False, str(exc))

    def get_video_body(self, video_id: str) -> Tuple[bytes, str]:
        """Get video body by id"""
        file_name = self._filename(video_id, self.BODY)
        if not os.path.isfile(file_name):
            return b'', 'FILE NOT FOUND'
        try:
            with open(file_name, mode='rb') as file:
                return (file.read(), '')
        except Exception as exc:
            return b'', str(exc)

    def get_video_data(self, video_id: str) -> Tuple[GetVideoResponse, str]:
        """Get video data by id - returns data and message"""
        file_name = self._filename(video_id, self.DATA)
        if not os.path.isfile(file_name):
            if os.path.isfile(self._filename(video_id, self.BODY)):
                return None, str(VideoStatus.Processing)

            return None, str(VideoStatus.Error)
        try:
            data = GetVideoResponse()
            if not data.load(file_name):
                raise Exception('failed to read video response', file_name)

            return (data, '')
        except Exception as exc:
            return None, str(exc)

    def update_video(self,
                     video_id: str,
                     video_data: BaseModel) -> Tuple[bool, str]:
        """Update video data, returning success, message"""
        video_file = self._filename(video_id, self.BODY)
        if os.path.isfile(video_file):
            os.unlink(video_file)
        file_name = self._filename(video_id, self.DATA)
        try:
            with open(file_name, 'w') as file:
                file.write(video_data.json())

            return (True, '')
        except Exception as exc:
            return (False, str(exc))

    def _filename(self, video_id: str, ext: str) -> str:
        return os.path.join(self._folder, f'video_{video_id}.{ext}')

    def get_video_file(self, video_id: str) -> str:
        return self._filename(video_id, self.BODY)

    def _purge_old_files(self):
        if time.time()-self._last_purge < 3600:
            return
        files = glob.glob(self._filename('*', '*'))

        for file in files:
            if time.time()-os.path.getmtime(file) > 3600:
                self._log.info('FileRepository purge: %s', file)
                os.unlink(file)
        self._last_purge = time.time()
