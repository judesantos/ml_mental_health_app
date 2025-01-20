
"""
This module is the entry point for the model builder application.

The module contains the main function that runs the model training pipeline.
"""

from ml.model.model_builder import ModelBuilderService


def main():
    """
    Run the model training pipeline.

    The function runs the model training pipeline to build and train the model.
    """
    print('Running model training...')

    # Create service
    svc = ModelBuilderService()
    svc.train_model()

    print('Model training complete.')


if __name__ == '__main__':
    main()
