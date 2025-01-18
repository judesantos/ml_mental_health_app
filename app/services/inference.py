"""
This model is the web service entry point for the machine learning predictive
model for apartment prices.

This module accepts a query parameter from the user and returns a prediction

- GET /predict/:
    Return a prediction of apartment prices from the query parameters int
    the request. Returns a dictionary containing the prediction result.
    Return HTTP 400 for invalid arguments

"""

import json
from dataclasses import asdict

from flask import Blueprint, abort, request
from pydantic import ValidationError

from ..src.model.apartment import Apartment
from app.services.inference import model_inference_service as model


bp = Blueprint('prediction', __name__, url_prefix='/pred')


@bp.get('/predict')
def get_prediction():
    """
    Get a prediction of apartment prices.

    Returns:
        dict: A dictionary containing the prediction result.
    """
    try:
        features = Apartment(**request.args)
    except ValidationError:
        abort(code=400, description='Bad input params')

    prediction = model.predict(
        list(features.model_dump().values()),
    )
    apartment_dict = asdict(features)
    apartment_dict['rent'] = prediction

    return json.dumps(apartment_dict, indent=0)
