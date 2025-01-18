"""
This module contains functions to prepare the dataset for model training.
"""

import pandas as pd
import re

from model.pipeline.collection import load_data_from_db


def prepare_df():
    """
    Load, Prepare data. Return dataframe

    Returns:
      pd.DataFrame: dataset
    """
    # Load dfset from collection
    data = load_data_from_db()
    df_encoded = encode_categorical_features(data)
    return reg_parse_garden(df_encoded.copy())


def encode_categorical_features(df):
    """
    One-hot encode specified columns

    Args:
      df: (pd.DataFrame) dataset
      columns: (list) columns to one-hot encode
      drop_first: (bool) drop first column

    Returns:
      pd.DataFrame: updated dataset
    """
    return pd.get_dummies(
        df,
        columns=['balcony', 'parking', 'furnished', 'garage', 'storage'],
        drop_first=True
    )


def reg_parse_garden(df):
    """
    Parse numeric values from feature 'garden'

    Args:
      df: (pd.DataFrame) dataset

    Returns:
      pd.DataFrame: updated dataset
    """

    df['garden'] = df['garden'].apply(
        lambda x: 0 if x == 'Not present' else int(re.findall(r'\d+', x)[0])
    )

    # Return the updated dataset.
    # Optional: The original input dataset would be the same instance
    return df
