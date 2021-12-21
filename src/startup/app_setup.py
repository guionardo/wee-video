from typing import Tuple

from fastapi import FastAPI
from src.abstractions.repository import RepositoryAbstraction
from src.abstractions.stats_service import StatsServiceAbstraction
from src.abstractions.video_processor import VideoProcessorAbstraction
from src.services.api_service import APIService
from src.services.file_repository import FileRepository
from src.services.stats_service import StatsService
from src.services.video_processor import VideoProcessor
from src.startup.config import Config, get_app_config


def app_setup(config: Config) -> Tuple[FastAPI,
                                       RepositoryAbstraction,
                                       StatsServiceAbstraction,
                                       VideoProcessorAbstraction,
                                       APIService]:
    app = FastAPI(**get_app_config())

    repository = FileRepository(config.repository_folder)
    stats = StatsService()
    processor = VideoProcessor(stats, repository)

    api_service = APIService(repository, stats, processor, config)

    return (app, repository, stats, processor, api_service)
