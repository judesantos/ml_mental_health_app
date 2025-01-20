"""
This module is used to load data from the database table onto a pandas
dataFrame for model training.

The module contains the following functions:
    - load_data_from_db: Load data from database
"""

import pandas as pd
from loguru import logger

from ml.config import db

from ml.db.mental_health import MentalHealthDbModel
from sqlalchemy import select


def load_data_from_db():
    """
    Load data from database

    If no data is found in the database, the function logs an error
    message and returns an empty DataFrame.

    Returns:
      pd.DataFrame: dataset
    """

    logger.info(f'Loading data from db(`{
                MentalHealthDbModel.__table__}`)...')

    query = select(MentalHealthDbModel)
    return pd.read_sql(query, db.engine)
