"""
This module provides the entry point to the model prediction application

The module contains the ModelService class, which is responsible for loading
a pre-trained model and making predictions.
"""

import pandas as pd
import xgboost as xgb

from typing import List, Dict

from pathlib import Path
import pickle as pk
from loguru import logger

from ml.config.model import model_settings as settings
from ml.model.pipeline.preparation import MentalHealthData

FEATURE_NAMES = [
    'POORHLTH', 'PHYSHLTH', 'GENHLTH', 'DIFFWALK', 'DIFFALON',
    'CHECKUP1', 'DIFFDRES', 'ADDEPEV3', 'ACEDEPRS', 'SDLONELY', 'LSATISFY',
    'EMTSUPRT', 'DECIDE', 'CDSOCIA1', 'CDDISCU1', 'CIMEMLO1', 'SMOKDAY2',
    'ALCDAY4', 'MARIJAN1', 'EXEROFT1', 'USENOW3', 'FIREARM5', 'INCOME3',
    'EDUCA', 'EMPLOY1', 'SEX', 'MARITAL', 'ADULT', 'RRCLASS3', 'QSTLANG',
    '_STATE', 'VETERAN3', 'MEDCOST1', 'SDHBILLS', 'SDHEMPLY', 'SDHFOOD1',
    'SDHSTRE1', 'SDHUTILS', 'SDHTRNSP', 'CDHOUS1', 'FOODSTMP', 'PREGNANT',
    'ASTHNOW', 'HAVARTH4', 'CHCSCNC1', 'CHCOCNC1', 'DIABETE4', 'CHCCOPD3',
    'CHOLCHK3', 'BPMEDS1', 'BPHIGH6', 'CVDSTRK3', 'CVDCRHD4', 'CHCKDNY2',
    'CHOLMED3'
]

EXPTECTED_FEATURE_ORDER = [
    'poorhlth', 'physhlth', 'genhlth', 'diffwalk', 'diffalon',
    'checkup1', 'diffdres', 'addepev3', 'acedeprs', 'sdlonely', 'lsatisfy',
    'emtsuprt', 'decide', 'cdsocia1', 'cddiscu1', 'cimemlo1', 'smokday2',
    'alcday4', 'marijan1', 'exeroft1', 'usenow3', 'firearm5', 'income3',
    'educa', 'employ1', 'sex', 'marital', 'adult', 'rrclass3', 'qstlang',
    'state', 'veteran3', 'medcost1', 'sdhbills', 'sdhemply', 'sdhfood1',
    'sdhstre1', 'sdhutils', 'sdhtrnsp', 'cdhous1', 'foodstmp', 'pregnant',
    'asthnow', 'havarth4', 'chcscnc1', 'chcocnc1', 'diabete4', 'chccopd3',
    'cholchk3', 'bpmeds1', 'bphigh6', 'cvdstrk3', 'cvdcrhd4', 'chckdny2',
    'cholmed3'
]


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

        self._load_model()

    def _load_model(self):
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

            logger.info(f'Loading model from {model_path}')
            with open(model_path, 'rb') as model_file:
                self.model = pk.load(model_file)

        except Exception as e:
            logger.error(f'Error loading model: {e}')

    def predict(self, batch: List[Dict[str, int]]):
        """
        Make a prediction using the pre-trained model

        The function takes a dictionary of parameters and returns predictions.
        The incoming batch of features will be reordered to match the
        model's expected feature column positions.

        Args:
          params: (dict) input parameters for prediction

        Returns:
          list: prediction
        """
        logger.info('Making predictions...')
        logger.debug(f'Data:\n {batch}')

        _batch = self._reorder_features(batch)
        batch_df = pd.DataFrame(_batch, columns=FEATURE_NAMES)

        # Prepare our inference data
        # MentalHealthData can process both feature with target data,
        # or just feature data
        # In this case, we are only interested in the feature data
        mh = MentalHealthData(batch_df)

        # XGb expects data in DMatrix format
        xgb_features = xgb.DMatrix(mh.get_data())

        # Make predictions
        return self.model.predict(xgb_features)

    def _reorder_features(self, batch: List[Dict[str, int]]):
        """
        Reorder input data to match the expected feature order.
        The submitted batch data is expected to be without missing values

        The reordering requires the incoming batch to be in dictionary format
        so as to be able to determine the feature names of each input value.
        Once the proper order is determnined, we can now do away with the
        column names in the batch and return only the values in
        the correct order.

        Args:
            data list[dict]: Input data as a dictionary.
            expected_order (list): List of features in the correct order.

        Returns:
            list[List]: Batch of features in the correct order.
        """

        ordered_batch = []

        for features in batch:
            _features = [int(features[feature])
                         for feature in EXPTECTED_FEATURE_ORDER]
            # Append the ordered feature values to the batch
            ordered_batch.append(_features)

        logger.debug(f'Ordered batch: {ordered_batch}')
        return ordered_batch
