"""
This module contains the login form.
Used to create the login form for the application.

Classes:
    LoginForm: A class used to create the login form for the application.
"""

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """
    LoginForm is used for user login.

    Attributes:
        username: A string field for the username.
        password: A password field for the password.
        submit: A submit field to submit the
    """
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Enter Username"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Enter Password"}
    )
    submit = SubmitField('Login')
