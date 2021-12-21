import logging
import logging.handlers
import os
import sys

from src import __toolname__
from src.startup.config import Config
from src.startup.utils import folder_exists_and_is_writeable


def setup_logging(config: Config):
    log = []
    fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'

    if config.log_folder:
        if not os.path.isdir(config.log_folder):
            log.append(f'log_folder "{config.log_folder}" not found')
            config.log_folder = ''
        else:
            suc, msg = folder_exists_and_is_writeable(config.log_folder)
            if not suc:
                config.log_folder = ''
                log.append(msg)

    formatter = logging.Formatter(fmt=fmt)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(config.log_level)
    logging.root.addHandler(console_handler)

    if config.log_folder:
        log_file = os.path.join(config.log_folder, __toolname__+'.log')
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file,
            when="midnight",
            interval=1,
            backupCount=10)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(config.log_level)
        logging.root.addHandler(file_handler)
        log.append(f'logging to file: {log_file}')

    if log:
        logger = logging.getLogger(__name__)
        for line in log:
            logger.warning(line)
