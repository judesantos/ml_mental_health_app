
"""
This module is the entry point for the model builder application.

The module contains the main function that runs the model training pipeline.
"""

from model.model_builder import ModelBuilderService
from loguru import logger


@logger.catch
def main():
    """
    Run the model training pipeline.

    The function runs the model training pipeline to build and train the model.
    """

    logger.info("Starting model builder application...")

    # Create service
    svc = ModelBuilderService()
    svc.train_model()


if __name__ == '__main__':
    main()
