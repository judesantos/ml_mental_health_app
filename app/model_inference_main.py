
"""
This module is the entry point for the model prediction application.
The module contains the main function that accepts unseen data to make
predictions.
"""

from model.model_inference import ModelInferenceService
from loguru import logger
import pandas as pd


@logger.catch
def main():
    """
    Application entry point. Run model prediction for apartment rental price.
    """

    logger.info('Running model prediction...')
    # Create service
    svc = ModelInferenceService()

    # Build test data DF
    columns = [
        'area',
        'constraction_year',
        'bedrooms',
        'garden',
        'balcony_yes',
        'parking_yes',
        'furnished_yes',
        'garage_yes',
        'storage_yes'
    ]
    test_data = [[85, 2015, 2, 20, 1, 1, 0, 0, 1]]
    test_df = pd.DataFrame(test_data, columns=columns)

    # Predict
    pred = svc.predict(test_df)
    # Print prediction
    logger.info(f'Predicted Rent: {pred}')


if __name__ == '__main__':
    main()
