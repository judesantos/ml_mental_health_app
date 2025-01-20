"""
This modle contains the configuration settings for the ML model.

THe module initializes the model configuration settings and
makes them available for the application.
"""

import os
from loguru import logger

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath


class ModelSettings(BaseSettings):
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

    # ML Model settings
    model_path: DirectoryPath
    model_name: str  # The mode base name

    def update(self, updates: dict):
        """
        Update the model settings with new values.
        """
        # Load current settings
        env_file_path = ModelSettings.model_config.get('env_file', '.env')
        logger.info(f"Updating .env file at: {env_file_path}")

        # Read the existing .env file into a dictionary
        env_variables = {}
        if os.path.exists(env_file_path):
            with open(env_file_path, "r") as file:
                for line in file:
                    # Skip comments and blank lines
                    if line.strip() and not line.strip().startswith("#"):
                        key, _, value = line.partition("=")
                        env_variables[key.strip()] = value.strip()

        # Update the dictionary with new values
        env_variables.update(updates)

        # Write the updated variables back to the .env file
        with open(env_file_path, "w") as file:
            for key, value in env_variables.items():
                file.write(f"{key}={value}\n")


model_settings = ModelSettings()
