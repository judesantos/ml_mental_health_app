"""
This module contains the main routes for the Flask app.

Implements the home route for the application.
Initializes the main blueprint for the application.
"""

from datetime import datetime

from extensions import limiter
from flask import Blueprint, render_template, url_for
from flask import redirect, flash
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_login import current_user

from ui.forms.ml_input_form import MlInputForm, DescriptiveSelectField
from ui.forms.ml_input_form import process_form


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
    form = MlInputForm()
    if form.validate_on_submit():
        # Run inference on the survey data here.
        if process_form(form):
            return render_template('report.html', form=form, datetime=datetime)

    # user = get_jwt_identity()
    return render_template('evaluation.html', current_user=current_user, form=form)


# @limiter.limit("5 per minute")
# @jwt_required()
# def evalution_report():
#    user = get_jwt_identity()
#    return render_template(
#        'report.html',
#        user=user,
#    )
