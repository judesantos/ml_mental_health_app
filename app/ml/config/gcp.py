"""
This modle contains the configuration settings for GCP.

THe module initializes the model configuration settings and
makes them available for the application.
"""

import os
from loguru import logger

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath


class GCPSettings(BaseSettings):
    """
    The model configuration settings class.

    The class initializes the model configuration settings for the application.
    The model settings are loaded from the .env file located in the root
    of the application.

    Attributes:
      model_path: (DirectoryPath) path to the model file
      model_name: (str) name of the model file
    """

    # Initialize config based on .env file
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    ai_backend: str
    gcp_project_id: str
    gcp_region: str
    gcp_service_name: str


gcp_settings = GCPSettings()
