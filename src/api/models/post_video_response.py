from pydantic import BaseModel


class PostVideoResponse(BaseModel):
    video_id: str
    average_processing_time: float


class PostVideoResponseError(BaseModel):
    message: str
