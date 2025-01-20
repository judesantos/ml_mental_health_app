
"""
This module is the entry point for the model prediction application.
The module contains the main function that accepts unseen data to make
predictions.
"""

import sys

import argparse
import json

from ml.model.model_inference import ModelInferenceService
from ml.model.model_inference import EXPECTED_FEATURE_ORDER


class ParsetArgumentError(argparse.ArgumentParser):
    def error(self, message):
        # Customize error message and usage display
        sys.stderr.write(f"\nError: {message}\n\n")
        self.print_help()  # Show usage
        sys.exit(2)  # Exit with error code 2


def process_args():
    """
    Terminal argument parser for the model inference application.
    """

    parser = argparse.ArgumentParser(
        description='''Enter inference data. Expects 55 integer
        items in you input list.'''
    )

    parser.add_argument(
        '--values',
        required=True,
        type=str,
        help="Enter string in JSON or CSV format"
    )

    values = []
    args = parser.parse_args()
    if args.values.startswith('['):
        # JSON format
        values = json.loads(args.values)
    else:
        # CSV format
        values = args.values.split(',')

    if len(values) != 55:
        print(f'Received {len(values)} list items.')
        parser.print_help()
        sys.exit(2)

    return values


def main():
    """
    Application entry point. Run model prediction for apartment rental price.
    """

    data = process_args()

    model_builder = ModelInferenceService()
    # Make a dictionary from the data list with
    # the expected feature order and name
    inference_data = dict(zip(EXPECTED_FEATURE_ORDER, data))

    predictions = model_builder.predict([inference_data])
    percentages = [p * 100 for p in predictions[0]]

    # Define prediction classes, and get the dominant class
    classes_dict = {0: '0 Days', 1: '1-13 Days', 2: '14+ Days', 3: 'Unsure'}
    dominant_class = classes_dict[percentages.index(max(percentages))]
    print(f'\n  Predicted: {dominant_class}')
    print(f'     0 Days: {percentages[0]:.2f}%')
    print(f'  1-13 Days: {percentages[1]:.2f}%')
    print(f'   14+ Days: {percentages[2]:.2f}%')
    print(f'     Unsure: {percentages[3]:.2f}%\n')


if __name__ == '__main__':
    main()
