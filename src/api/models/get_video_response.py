"""Video Data Response"""

import json
import logging
from typing import Optional

from pydantic import BaseModel
from src.api.models.video_categories import VideoCategory
from src.api.models.video_status import VideoStatus


class GetVideoResponse(BaseModel):
    """Video Data Model"""

    video_id: Optional[str]
    status: Optional[VideoStatus]
    categories: Optional[VideoCategory]
    message: Optional[str]
    processing_time: Optional[float]

    def load(self, filename: str) -> bool:
        try:
            with open(filename, encoding='ascii') as file:
                data = json.loads(file.read())
            new = GetVideoResponse(**data)
            self.video_id = new.video_id
            self.status = new.status
            self.categories = new.categories
            self.processing_time = new.processing_time

            return True
        except Exception as exc:
            logging.getLogger(__name__).error(
                'Failed to read video processing data @ %s - %s', filename, exc)
        return False

    def save(self, filename: str) -> bool:
        try:
            with open(filename, encoding='ascii') as file:
                file.write(self.json(ensure_ascii=True, exclude=['message']))
            return True
        except Exception as exc:
            logging.getLogger(__name__).error(
                'Failed to write video processing data @ %s - %s', filename, exc)
        return False
