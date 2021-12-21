"""Configuration setup"""
import os
import dotenv

from src import (__author__, __author_email__, __description__, __toolname__,
                 __version__)
from src.startup.utils import folder_exists_and_is_writeable

MEGABYTE = 1 << 20


class Config:
    """Configuration Class"""

    def __init__(self):
        dotenv.load_dotenv()
        self.repository_folder = os.getenv('REPOSITORY', '.repository')
        self.log_folder = os.getenv('LOG_FOLDER', '')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.port = os.getenv('PORT', '8080')
        self.max_file_size = os.getenv('MAX_FILE_SIZE', str(20*MEGABYTE))

    def validate(self):
        """Check if configuration is valid"""
        self.repository_folder = os.path.abspath(self.repository_folder)
        suc, msg = folder_exists_and_is_writeable(self.repository_folder)
        if not suc:
            raise ConfigurationException(msg)
        self._validate_int('port')
        self._validate_int('max_file_size')

    def _validate_int(self, property: str):
        raw_value = getattr(self, property)
        try:
            value = int(raw_value)
            setattr(self, property, value)
        except ValueError as exc:
            raise ConfigurationException(
                f'invalid {property.upper()} "{raw_value}"') from exc


class ConfigurationException(Exception):
    """Configuration Exception class"""
    ...


def get_app_config() -> dict:
    """Returns FastAPI configuration"""
    app_config = dict(
        title=__toolname__,
        description=__description__,
        version=__version__,
        contact=dict(
            name=__author__,
            email=__author_email__
        )
    )
    return app_config
