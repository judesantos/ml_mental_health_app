"""
The module contains the settings class that provides the environment
variables of the application.

The settings class is used to initialize the configuration settings
for the application. Configuration values are loaded from the .env file
located in the root of the application execution path.
"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """
    The settings class is used to initialize the configuration
    settings key/value pairs required by the application.

    Attributes:
        SECRET_KEY: (str) secret key for the application
        JWT_COOKIE_SECURE: (bool) secure flag for JWT cookie
        JWT_SECRET_KEY: (str) secret key for JWT token
        MAX_CONTENT_LENGTH: (int) maximum content length
        SQLALCHEMY_DATABASE_URI: (str) database connection URI
        SQLALCHEMY_TRACK_MODIFICATIONS: (bool) track modifications
        GOOGLE_CLIENT_ID: (str) Google client ID
        GOOGLE_CLIENT_SECRET: (str) Google
        MAX_CONTENT_LENGTH: (int) maximum content length
    """

    ENV: str
    SERVER_NAME: str

    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_COOKIE_SECURE: bool
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_DISCOVERY_URL: str
    MAX_CONTENT_LENGTH: int

    @field_validator('MAX_CONTENT_LENGTH', mode='before', check_fields=False)
    def parse_max_content_length(cls, v):
        """
        Convert the max content length to Integer.
        Perform arithmetic operation when needed (e.g.: 2 * 2).
        """
        if isinstance(v, str):
            return eval(v)

    @field_validator(
        'SQLALCHEMY_DATABASE_URI',
        mode='before',
        check_fields=False
    )
    def parse_sqlite_db_path(cls, v):
        """
        Convert the SQLite database path to an absolute path.
        Prepend the SQLite URI to the absolute path, if not present.
        """

        db_path = v
        sqlite_uri = 'sqlite:///'

        db_path = db_path[len(sqlite_uri):]
        db_path = sqlite_uri + os.path.abspath(db_path)

        return db_path

    # Initialize config based on .env file
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = Settings()
