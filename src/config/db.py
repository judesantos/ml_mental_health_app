"""
This module contains database configuration settings, database connection
setup.

The module initializes the database configuration settings and connection
setup for the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath

import sys
from loguru import logger

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


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

    # Database settings
    db_path: DirectoryPath
    db_name: str
    db_debug: bool


# 2. Initialize Db settings

try:
    db_settings = DbSettings()

    logger.debug("Setting up Db engine...")

    db_path = f'{db_settings.db_path}/{db_settings.db_name}'
    logger.debug(f"Database path: {db_path}")

    engine = create_engine(
        'sqlite:///' + db_path,
        echo=db_settings.db_debug
    )

    logger.debug("Setup Db engine successful.")

except Exception as e:
    logger.error(f"Config init() failed: {e}")
    sys.exit(1)  # Force exit if connection fails


# 3. Test database connection, tables

try:
    logger.debug("Testing database connection...")

    with engine.connect() as connection:
        logger.info("DB Connection successful!")

except Exception as e:
    logger.error(f"Db Connection failed: {e}")
    sys.exit(2)

try:
    logger.debug("Testing database tables...")

    with Session(engine) as session:

        result = session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result]

        if len(tables) == 0:
            logger.error("No tables found in the database.")
            sys.exit(3)
        else:
            logger.debug("Tables in the database:", tables)

except Exception as e:
    logger.error(f"Session.execute() failed: {e}")
    sys.exit(4)
