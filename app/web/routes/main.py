"""
This module contains the main routes for the Flask app.

Implements the home route for the application.
Initializes the main blueprint for the application.
"""
from datetime import datetime
from loguru import logger

from flask import Blueprint, render_template, request
from flask import flash, redirect, url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_login import current_user

from web.extensions import limiter

from web.templates.ui.forms.ml_input_form import MlInputForm, prediction_report
from web.templates.ui.forms.ml_input_form import process_form

from ml.model.model_inference import ModelInferenceService


bp = Blueprint('main', __name__)


@bp.route('/')
@limiter.limit("100 per minute")
def home():
    return render_template(
        'home.html',
    )


@bp.route('/evaluation', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
@jwt_required()
def evaluation():

    user = get_jwt_identity()
    form = MlInputForm()

    if form.validate_on_submit():

        logger.debug(
            'Evaluation submission: addr: '
            f'{request.remote_addr}, uid: {user}',
        )

        try:
            # Run inference on this request
            # ml_features = MlModelFeatures(**form.data)
            model_builder = ModelInferenceService()
            logger.debug(f'Running model inference...')
            predictions = model_builder.predict([form.data])
            logger.info(f'Prediction resuls: {predictions}')

            # Generate the report data and chart
            data, chart_url = prediction_report(predictions[0].tolist())

            if process_form(form):
                # process_form() did the work for us to update the
                # form poperties of each field ('selected'), we need
                # this in the report page and show the user's input

                # Send the update form to the report template
                return render_template(
                    'report.html',
                    form=form,
                    data=data,
                    chart_url=chart_url,
                    datetime=datetime
                )
            else:
                logger.error(
                    f'Error processing the form: addr: {request.remote_addr}, '
                    f'uid: {user}'
                )
                return render_template(
                    'evaluation.html',
                    current_user=current_user,
                    form=form
                )

        except Exception as e:
            logger.error(f'Model inference error: {e.with_traceback(None)}')
            # Send a flash message back to the originating page
            now = datetime.now()
            msg_date = now.strftime("%A, %b. %d %-I:%M:%S %p")
            flash(
                f'{msg_date} - '
                'Error processing the form. Please try again.', 'danger'
            )
            return render_template(
                'evaluation.html',
                current_user=current_user,
                form=form
            )

    logger.debug(f'Evaluation request: addr: {request.remote_addr}')
    return render_template(
        'evaluation.html',
        current_user=current_user,
        form=form
    )
