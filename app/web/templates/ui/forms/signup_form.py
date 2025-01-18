"""
This module contains the SignupForm class, a subclass of FlaskForm.
Used to create the signup form for the application.

Classes:
    SignupForm: A class used to create the signup form for the application.
"""

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp


class SignupForm(FlaskForm):
    """
    SignupForm is used for user registration

    Attributes:
        username: A string field for the username.
        email: A string field for the email.
        phone: A string field for the phone number.
        password: A password field for the password.
        confirm_password: A password field to confirm the password.
        submit: A submit field to submit
    """

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Enter Username"}
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                message="Invalid email address."
            )
        ],
        render_kw={"placeholder": "Enter Email"}
    )
    phone = StringField(
        'Phone',
        validators=[
            DataRequired(),
            Regexp(
                r'^\+?[1-9]\d{1,14}$',
                message="Invalid phone number. \
                Please use international format (+1234567890)."
            )
        ],
        render_kw={"placeholder": "Enter Phone"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Enter Password"}
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo(
            'password', message='Passwords must match.')],
        render_kw={"placeholder": "Confirm Password"}
    )
    submit = SubmitField('Sign Up')
