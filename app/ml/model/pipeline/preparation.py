"""
This module prepares (preprocessing) the dataset for model training

We define here the different characteristics of the dataset we want to
provde to the model.

The module contains the following functions:
    - prepare_df: Load, prepare data
"""

from loguru import logger
from app.ml.model.pipeline.collection import load_data_from_db


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

        # 1. Make a copy of the dataset
        self._df = df.copy()

        # Integrate composite features
        self._integrate_composite_features()

        # 2. Define the target variable
        self.target = '_MENT14D'

        # Define the feature groups

        # 3. Numeric features need scaler
        continuous_features = ['PHYSHLTH', 'POORHLTH', 'MARIJAN1']
        aggregated_features = [
            'Mental_Health_Composite',
            'Income_Education_Interaction',
            'Physical_Mental_Interaction',
        ]
        non_categorical_features = continuous_features + aggregated_features

        # 4. Categorical features
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

    def _integrate_composite_features(self):
        # Create a new copy of the cleaned dataset
        mental_health_features = ['EMTSUPRT', 'ADDEPEV3', 'POORHLTH']
        # Using Nonlinear interaction
        self._df['Physical_Mental_Interaction'] = self._df['GENHLTH'].astype(
            int) * self._df['PHYSHLTH']
        # Income and Education Interaction
        self._df['Income_Education_Interaction'] = self._df['INCOME3'].astype(
            int) * self._df['EDUCA'].astype(int)
        # Mental Health
        self._df['Mental_Health_Composite'] = self._df[
            mental_health_features
        ].mean(axis=1)


def _prepare_df():
    """
    Load, Prepare data. Return dataframe

    Returns:
      pd.DataFrame: dataset
    """
    # Load dataset from collection
    df = load_data_from_db()
    # Remove the column id
    df.drop('id', axis=1, inplace=True)

    logger.debug('Loaded data from db successfully.')

    return df


def get_mental_health_data() -> MentalHealthData:
    """
    Load and prepare the dataset

    Returns:
      MentalHealthData: dataset characteristics
    """
    df = _prepare_df()
    return MentalHealthData(df)
