"""
This module contains the UserInferenceLog model which is used
to store the logs of the user's inference inputs.
"""
from sqlalchemy import Integer, Column
from web.extensions import db


class UserInferenceLog(db.Model):

    __tablename__ = 'user_inference_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'app_user.id'), nullable=False)
    inference_id = db.Column(db.Integer, db.ForeignKey(
        'cdc_inference_data.id'), nullable=False)
    log_date = db.Column(db.DateTime, default=db.func.now())
    description = db.Column(db.String(255), nullable=True)
    purpose = db.Column(db.String(100), nullable=True)

    # Relationships
    user = db.relationship(
        'User',
        back_populates='logs'
    )
    inference = db.relationship(
        'MentalHealthDbInferenceModel',
        back_populates='logs'
    )
