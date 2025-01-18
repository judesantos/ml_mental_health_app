"""
This module contains the main routes for the Flask app.

Implements the home route for the application.
Initializes the main blueprint for the application.
"""

from datetime import datetime

from flask import Blueprint, render_template, request
from flask import redirect, flash
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_login import current_user

from web.extensions import limiter

from web.templates.ui.forms.ml_input_form import MlInputForm
from web.templates.ui.forms.ml_input_form import process_form

from loguru import logger

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
        # Run inference on the survey data here.
        if process_form(form):
            logger.debug(
                'Evaluation report: addr: '
                f'{request.remote_addr}, uid: {user}',
            )
            return render_template(
                'report.html',
                form=form,
                datetime=datetime
            )
        else:
            logger.error(
                f'Error processing the form: addr: {request.remote_addr}, '
                f'uid: {user}'
            )
            flash('Error processing the form. Please try again.', 'danger')
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

