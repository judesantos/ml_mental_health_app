"""
Thids module contains application configuration settings, database connection,
and logger setup.

The module initializes the configuration settings, database connection,
and logger for the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

import sys
from loguru import logger

# 1. Configuration logging settings

settings = None
engine = None


class LoggingSettings(BaseSettings):
    """
    The logging configuration settings class.

    The class initializes the logging configuration settings for the
    application. Key settings are loaded from the .env file located in
    the root of the application execution path.
    Once the settings are loaded, the logger is configured for file
    and console logging.

    Attributes:
      log_path: (str) path to the log file
      log_rotation: (str) log file rotation setting
      log_compression: (str) log file compression setting
      log_retention: (str) log file retention setting
      log_file_name: (str) name of the log file
      log_file_level: (str) log file level setting
      log_console_level: (str) console log level setting
    """

    # Initialize config based on .env file
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Logging settings
    log_path: str
    log_rotation: str
    log_compression: str
    log_retention: str
    log_file_name: str
    log_file_level: str
    log_console_level: str


# 2. Initialize logging

def configure_logging():
    """
    Configure the logging for the application.

    This function initializes the logger for the application based
    on the logging settings loaded from the .env file.
    The logger is configured for file and console logging.

    Args:
      log_level: (str) log level
    """

    logger.info('Initializing logger...')

    settings = LoggingSettings()
    logger.remove()  # Remove default logger

    log_format = (
        '<green>{time:YYYY-MM-DD HH:mm:ss}</green>|'
        '<level>{level}</level>|'
        '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>|'
        '<yellow>tid:{thread.id}</yellow>: '
        '<level>{message}</level>'
    )

    # Setup App console logger
    logger.add(sys.stdout, level=f'{settings.log_console_level}')

    # Setup App file logger
    logger.add(
        f'{settings.log_path}/{settings.log_file_name}',
        format=log_format,
        rotation=f'{settings.log_rotation}',
        compression=f'{settings.log_compression}',
        retention=f'{settings.log_retention}',
        level=f'{settings.log_file_level}'
    )

    logger.debug("Logger initialized.")


configure_logging()
