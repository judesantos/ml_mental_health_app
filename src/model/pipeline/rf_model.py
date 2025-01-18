
"""
This module provides the model training pipeline.

The module contains functions to prepare the dataset,
train the model, and save the model.
"""

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor

import pickle as pkl
from loguru import logger

from model.pipeline.preparation import prepare_df
from config import model_settings as settings


def build_model():
    """
    Train model given a dataset, then save the model

    The function loads the preprocessed dataset,
    splits the dataset into training and testing sets,
    trains the model using the training set, evaluates the model
    using the test set, and saves the model.

    Returns:
      float: model score
    """

    logger.info('Building model...')

    # Load the preprocessed dataset
    df = prepare_df()
    # Identify X and y
    X, y = get_X_y(df)
    # Split the dataset
    X_train, X_test, y_train, y_test = split_train_test(X, y)

    logger.debug(f'X_train={X_train.shape}, y_train={y_train.shape}.')

    # Train the model
    logger.info('Training model...')
    rf = train_model(X_train, y_train)
    # Evaluate the model
    score = evaluate_model(rf, X_test, y_test)
    logger.info(f'Model score: {score:.3f}')
    # Save the model
    save_model(rf)
    # return optimized model score
    return score


def get_X_y(
        data,
        col_X=[
            'area',
            'constraction_year',
            'bedrooms',
            'garden',
            'balcony_yes',
            'parking_yes',
            'furnished_yes',
            'garage_yes',
            'storage_yes'
        ],
        col_y='rent'):
    """
    Return X, y from the source dataframe
    """
    return data[col_X], data[col_y]


def split_train_test(X, y):
    """
    Split train, test sets.

    Args:
      X: (array) features
      y: (array) target values

    Return:
      X_train, X_test, y_train, y_test
    """
    return train_test_split(X, y, test_size=0.2)


def train_model(X_train, y_train):
    """
    This function trains a model using the training set and
    returns the trained model.

    The function uses GridSearchCV to find the best hyperparameters
    for the model, then return the best model, with the best hyperparameters.

    Args:
      X_train: (array) training set features
      y_train: (array) training set target

    Returns:
      object: trained model
    """

    # Define hyperparameters to train on
    grid_space = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 6, 9, 12]
    }

    logger.info(
        f'Grid search space for RandomForesetClassifier: '
        f'{grid_space}',
    )

    grid = GridSearchCV(
        RandomForestRegressor(),
        param_grid=grid_space,
        cv=5,
        scoring='r2'
    )

    logger.info(f'GridSearchCV params: {grid.get_params()}')

    # Run grid search - train using each hyper param values in range
    model_grid = grid.fit(X_train, y_train)

    logger.info(
        'Model Hyperparameter best parameter/values: '
        f'{model_grid.best_params_}',
    )

    # Return best model
    return model_grid.best_estimator_


def evaluate_model(model, X_test, y_test):
    """
    This function evaluates the model using the test set and returns the score.

    Args:
      model: (object) trained model
      X_test: (array) test set features
      y_test: (array) test set target values

    Returns:
      float: model score
    """
    return model.score(X_test, y_test)


def save_model(model):
    """
    Save model to disk
    The function saves the trained model to the specified path using pickle.

    Args:
      model: (object) trained model
    """

    logger.info(
        'Saving model to '
        f'{settings.model_path}/{settings.model_name}',
    )

    pkl.dump(model, open(f'{settings.model_path}/{settings.model_name}', 'wb'))
