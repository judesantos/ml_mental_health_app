"""
This module provides the entry point to the model prediction application

The module contains the ModelService class, which is responsible for loading
a pre-trained model and making predictions.
"""

from loguru import logger

from model.pipeline.rf_model import build_model
from config import model_settings as settings


class ModelBuilderService:
    """
    A service class for building and saving the ML model.

    The class provides an interface to build a model and
    The class builds the model using the build pipeline.

    Attributes:
      model_path: path to save the model
      model_name: name

    Methods:
      train_model: Build and train a  model
    """

    def __init__(self):
        logger.debug('Initializing ModelBuilderService...')
        logger.debug(f'Model Name: {settings.model_name}')
        self.model_path = settings.model_path
        self.model_name = settings.model_name

    def train_model(self):
        """
        Train a model from specified path.

        The function builds and trains a model from the specified path,
        The model is saved to the specified path

        Returns:
          None
        """

        logger.debug('Training model...')

        # Build, train and save model
        build_model()

        logger.debug('Training successful')
        logger.debug(f'Saved model into {self.model_path}/{self.model_name}')
