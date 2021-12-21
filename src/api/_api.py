"""API definition"""
import logging
import sys

from fastapi import BackgroundTasks, File, status
from fastapi.responses import JSONResponse
from src.api.models.get_video_response import GetVideoResponse
from src.api.models.post_video_response import (PostVideoResponse,
                                                PostVideoResponseError)
from src.api.models.stats_response import StatsResponse
from src.startup.app_setup import app_setup
from src.startup.config import Config
from src.startup.logging import setup_logging

config = Config()
setup_logging(config)

try:
    config.validate()
except Exception as exc:
    logging.error(exc)
    sys.exit(1)

(app,
 repository,
 stats,
 video_processor,
 api_service) = app_setup(config)


@app.post('/video', status_code=202,
          responses={202: {"model": PostVideoResponse},
                     406: {"model": PostVideoResponseError}})
async def video_upload(file: bytes = File(...),
                       background_tasks: BackgroundTasks = None):
    video_id, process_time, message = api_service.receive_video(file)
    if video_id:
        if background_tasks:
            background_tasks.add_task(api_service.process_video, video_id)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=PostVideoResponse(
                video_id=video_id,
                average_processing_time=process_time).dict()
        )
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content=PostVideoResponseError(
            message=message).dict()
    )


@app.get('/video/{video_id}', response_model=GetVideoResponse)
async def video_get_info(video_id: str):
    return api_service.get_video_info(video_id)


@app.get('/stats', response_model=StatsResponse)
async def get_stats():
    return api_service.get_stats()
