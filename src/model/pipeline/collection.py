"""
This module is responsible for loading data from a file or a database.
"""

import pandas as pd
from loguru import logger

from config import engine
from db.rent_apartment import RentApartment
from sqlalchemy import select


def load_data_from_db():
    """
    Load data from database

    Returns:
      pd.DataFrame: data
    """

    logger.info('Loading data from database...')
    query = select(RentApartment)

    return pd.read_sql(query, engine)
