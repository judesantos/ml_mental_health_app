"""
This module provides the entry point to the model prediction application

The module contains the ModelService class, which is responsible for loading
a pre-trained model and making predictions.
"""

from pathlib import Path
import pickle as pk
from loguru import logger

from config import model_settings as settings


class ModelInferenceService:
    """
    A service class for managing the ML model.

    The class provides an interface to load a pre-trained model and
    make predictions. When the model is not found at the specified path,
    the class builds the model using the training pipeline.

    Attributes:
      model: pre-trained model

    Methods:
      load_model: Load a pre-trained model from config path
      predict: Make a prediction using the pre-trained model
    """

    def __init__(self):
        self.model = None
        self.model_path = settings.model_path
        self.model_name = settings.model_name

    def load_model(self):
        """
        Load a pre-trained model from config path

        The function loads a pre-trained model from the specified path,
        when the model is not found at the specified path,
        the function builds the model.

        Returns:
          None
        """

        try:
            logger.info('Loading model...')

            model_path = Path(f'{self.model_path}/{self.model_name}')
            with open(model_path, 'rb') as model_file:
                self.model = pk.load(model_file)
        except Exception as e:
            logger.error(f'Error loading model: {e}')

    def predict(self, params):
        """
        Make a prediction using the pre-trained model

        The function takes a dictionary of parameters and returns predictions.

        Args:
          params: (dict) input parameters for prediction

        Returns:
          list: prediction
        """
        logger.info('Making prediction...')
        logger.debug(f'Data:\n {params}')
        return self.model.predict(params)
