"""
This module contains database configuration settings, database connection
setup.

The module initializes the database configuration settings and connection
setup for the application.
"""

import os
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from loguru import logger
from sqlalchemy import create_engine


# 1. Configuration Db settings

db_settings = None
engine = None


class DbSettings(BaseSettings):
    """
    The database configuration settings.

    The class initializes the database configuration settings
    for the application.
    The database settings are loaded from the .env file located in the root
    of the application execution path.
    Once the settings are loaded, the database connection is established
    using the SQLAlchemy engine.

    Attributes:
      db_path: (DirectoryPath) path to the database
      db_name: (str) name of the database
      db_debug_config: (bool) debug setting for the
    """

    # Initialize config based on .env file
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    sqlalchemy_database_uri: str
    db_debug: bool = Field(..., alias="sqlalchemy_track_modifications")


# 2. Initialize Db settings

try:
    db_settings = DbSettings()

    logger.debug("Setting up Db engine...")

    database_uri = os.getenv(
        'DATABASE_URL', db_settings.sqlalchemy_database_uri)

    logger.debug(f"Database path: {database_uri}")

    engine = create_engine(
        database_uri,
        echo=db_settings.db_debug
    )

    logger.debug("Setup Db engine successful.")

except Exception as e:
    logger.error(f"Config init() failed: {e}")
    sys.exit(1)  # Force exit if connection fails
