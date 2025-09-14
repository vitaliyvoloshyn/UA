from loguru import logger
from .settings import file_retention, file_rotation, logging_file, logging_level

logger.add(logging_file, rotation=file_rotation, retention=file_retention, level=logging_level)
