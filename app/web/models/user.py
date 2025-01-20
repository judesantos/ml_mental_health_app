"""
This file contains the Db models for the application.

Classes:
    User: The User class defines the db user model.
"""

import bcrypt

from flask_login import UserMixin
from web.extensions import db


class User(db.Model, UserMixin):
    """
    The User class defines the db user model provided
    for application access and security.

    Attributes:
        id: The user id.
        username: The username for the user.
        password: The password hash for the user.
        email: The email for the user.
        phone: The phone number for the user.

    Methods:
        set_password: Set the password hash for the user.
        check_password: Check the password hash for the user.
    """
    __tablename__ = 'app_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    def set_password(self, password: str):
        """Set the password hash for the user."""
        self.password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        return self

    def check_password(self, password: str):
        """Check the password for the user."""
        password_good = bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )
        return password_good

     # Relationships
    logs = db.relationship(
        'UserInferenceLog',
        back_populates='user',
        cascade='all, delete-orphan'
    )
