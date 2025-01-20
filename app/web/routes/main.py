"""
This module contains the main routes for the Flask app.

Implements the home route for the application.
Initializes the main blueprint for the application.
"""

from datetime import datetime
from loguru import logger

from flask import Blueprint, render_template, request, session
from flask import flash, redirect, url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_login import current_user

from web.extensions import limiter
from web.models.mental_health_inference import MentalHealthDbInferenceModel
from web.extensions import db

from web.templates.ui.forms.ml_input_form import MlInputForm, prediction_report
from web.templates.ui.forms.ml_input_form import process_form

from ml.model.model_inference import ModelInferenceService
from web.models.user_inference_log import UserInferenceLog

from web.extensions import cache_get, cache_push


bp = Blueprint('main', __name__)


@bp.route('/')
@limiter.limit("100 per minute")
def home():
    return render_template(
        'home.html',
    )


@bp.route('/report', methods=['GET'])
@limiter.limit("100 per minute")
@jwt_required()
def report():

    logger.debug(f'Report request: addr: {request.remote_addr}')
    key = request.args.get('key')

    data = cache_get(key)
    if data:
        return render_template(
            'report.html',
            form=data['form'],
            data=data['data'],
            chart_url=data['chart_url']
        )
    else:
        flash('Report is expired and no longer accessible.', 'danger')
        return redirect(url_for('main.evaluation'))


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
            # 1. Run inference on this request
            model_builder = ModelInferenceService()
            logger.debug(f'Running model inference...')

            predictions = model_builder.predict([form.data])
            logger.info(f'Prediction resuls: {predictions}')

            # 2. Generate the report data and chart
            data, chart_url = prediction_report(predictions[0].tolist())

            # 3. Save the inference data in the db, and log the event

            # Save the inference data in the database
            inference = MentalHealthDbInferenceModel()
            # Automatically assigns matching fields
            form.populate_obj(inference)
            db.session.add(inference)
            db.session.commit()

            # Log the inference event
            log = UserInferenceLog(
                user_id=current_user.id,
                inference_id=inference.id,
                description=str(data),
                purpose=""
            )
            db.session.add(log)
            db.session.commit()

            # 4. Send the update form to the report template
            process_form(form)
            # process_form() did the work for us to update the
            # form poperties ('selected'), we need
            # this in the report page to show the user's input

            key = cache_push({
                'form': form,
                'data': data,
                'chart_url': chart_url
            })
            return redirect(url_for('main.report', key=key))

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
                form=form
            )

    logger.debug(f'Evaluation request: addr: {request.remote_addr}')
    return render_template(
        'evaluation.html',
        current_user=current_user,
        form=form
    )
