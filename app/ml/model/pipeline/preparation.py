"""
This module prepares (preprocessing) the dataset for model training

We define here the different characteristics of the dataset we want to
provde to the model.

The module contains the following functions:
    - prepare_df: Load, prepare data
"""

from loguru import logger
from model.pipeline.collection import load_data_from_db


class MentalHealthData():
    """
    Mental Health Data class defines the dataset characteristics including
    the feature groups by type and the target variable

    Attributes:
      target (str): target variable
      categorical_features (list): list of categorical features
    """

    def __init__(self, df):
        """
        Initialize the dataset and define the dataset characteristics

        Task:
          - Load and prepare the dataset
          - Define the dataset characteristics
        """

        # Reference the dataset
        self._df = df

        # Define the target variable
        self.target = '_MENT14D'

        # Define the feature groups

        # 1. Numeric features need scaler
        continuous_features = ['PHYSHLTH', 'POORHLTH', 'MARIJAN1']
        aggregated_features = [
            'Mental_Health_Composite',
            'Income_Education_Interaction',
            'Physical_Mental_Interaction',
        ]
        non_categorical_features = continuous_features + aggregated_features

        # 2. Categorical features
        self.categorical_features = [
            col for col in self._df.columns
            if col not in (non_categorical_features + [self.target])
        ]

    def get_data(self):
        """
        Return the dataset

        Returns:
          pd.DataFrame: dataset
        """
        return self._df


def _prepare_df():
    """
    Load, Prepare data. Return dataframe

    Returns:
      pd.DataFrame: dataset
    """
    # Load dataset from collection
    df = load_data_from_db()

    logger.debug('Loaded data from db successfully.')

    return _integrate_composite_features(df)


def _integrate_composite_features(df):
    # Create a new copy of the cleaned dataset
    _df = df.copy()

    mental_health_features = ['EMTSUPRT', 'ADDEPEV3', 'POORHLTH']
    # Using Nonlinear interaction
    _df['Physical_Mental_Interaction'] = _df['GENHLTH'].astype(
        int) * _df['PHYSHLTH']
    # Income and Education Interaction
    _df['Income_Education_Interaction'] = _df['INCOME3'].astype(
        int) * _df['EDUCA'].astype(int)
    # Mental Health
    _df['Mental_Health_Composite'] = _df[mental_health_features].mean(axis=1)

    return _df


def get_mental_health_data() -> MentalHealthData:
    """
    Load and prepare the dataset

    Returns:
      MentalHealthData: dataset characteristics
    """
    df = _prepare_df()
    return MentalHealthData(df)
