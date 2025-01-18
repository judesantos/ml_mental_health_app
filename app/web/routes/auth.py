"""
This module contains the routes for user authentication.

The module contains the routes for user registration, login,
and protected routes.

Entry points:
    - register: Register a new user.
    - login: Login a user.
    - login_google: Login with Google.
    - authorize_google: Authorize Google login.
    - protected: Protected route.
"""

from flask import Blueprint, request, jsonify, url_for, flash
from flask import session, redirect, render_template
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import unset_jwt_cookies, set_access_cookies
from flask_login import login_user, logout_user

from web.extensions import db, oauth, limiter
from web.settings import settings
from web.models.user import User

from web.templates.ui.forms.signup_form import SignupForm
from web.templates.ui.forms.login_form import LoginForm

from loguru import logger

bp = Blueprint('auth', __name__)


# Configure Google OAuth
# Register the Google OAuth client
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)


@bp.route('/login/google')
@limiter.limit("100 per minute")
def login_google():
    """
    This functin redirect the user authentication to the Google login page.
    When the user selects to login with Google. The front end should
    redirect the user to this route.

    Returns:
        Redirection link to Google login page.
    """
    redirect_uri = url_for('auth.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
    # return oauth.google.authorize_redirect(
    #    callback=url_for('authorize_google', _external=True)
    # )


@bp.route('/authorize/google')
@limiter.limit("100 per minute")
def authorize_google():
    """
    Google login callback function.
    This function is called after the user has successfully authenticated
    with Google.

    Saves the user information to the database if the user is not already
    registered. Creates an access token for the user.

    Returns:
        400: If the Google login failed.
        200: If the Google login is successful
    """

    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)

    if not user_info:
        return jsonify({"message": "Google login failed"}), 400

    email = user_info['email']
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(username=user_info['name'], email=email)
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity=user.username)
    return jsonify({
        "message": "Google login successful", "access_token": access_token
    }), 200


@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def login():
    """
    Login registed user with the provided username and password.
    The username and password are required parameters in the request body.
    When the user is successfully authenticated, an access token is created.

    Returns:
        401: If the username or password are invalid.
        200: If the user is successfully authenticated
    """
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        try:
            validation_success = True
            # Check if the user exists by validating username
            user = User.query.filter_by(username=username).first()
            if not user:
                # User may have registered with email
                user = User.query.filter_by(email=username).first()
            if user:
                # User found, check password
                if user.check_password(password=password):
                    session['user_id'] = user.id
                    # Validation successful, create access token and
                    # redirect to the dashboard
                else:
                    validation_success = False
            else:
                validation_success = False

            if validation_success is False:
                logger.warning(f'Login failed: addr: {request.remote_addr}')
                flash('Invalid username or password', 'danger')

                return redirect(url_for('auth.login'))

        except Exception as e:
            logger.error(f'Database exception: {str(e)}')
            flash(
                'Server encountered a problem, please try again.',
                category='danger'
            )

            return redirect(url_for('auth.login'))

        # Login successful, redirect to the dashboard
        login_user(user)
        response = redirect(url_for('main.evaluation'))

        # Set session cookie credentials,
        # otherwise the authenticated access to the resource we're
        # redirecting to will fail
        # See: jwt_required() decorator in the dashboard route
        access_token = create_access_token(identity=user.username)
        set_access_cookies(response, access_token)

        logger.debug(
            f'Login Success. addr: {request.remote_addr}, uid: {user.id}'
        )

        return response

    logger.debug( f'Login request: addr: {request.remote_addr}')
    return render_template('login.html', form=form)


@bp.route('/logout', methods=['get'])
@limiter.limit("100 per minute")
@jwt_required()
def logout():
    """
    Logout the currently authenticated user.
    The access token is invalidated by removing the JWT cookies.

    Redirects to the home page after logout.
    """

    logger.debug(f'Logout request. addr: {request.remote_addr}')

    logout_user()
    session.clear()

    response = jsonify({"msg": "Logout successful"})
    response.headers['Cache-Control'] = \
        'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.delete_cookie('remember_token')

    # Remove JWT cookies to invalidate the session
    unset_jwt_cookies(response)

    logger.debug(f'Logout request complete. addr: {request.remote_addr}')
    return redirect(url_for('main.home'))


@bp.route('/signup', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def signup():

    form = SignupForm()
    if form.validate_on_submit():

        print('Form validated')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        phone = form.phone.data

        try:
            # Check if user already exists
            existing_user = User.query.filter(User.email == email).first()
            if existing_user:
                flash('Email exists.', 'error')
            else:
                existing_user = User.query.filter(User.phone == phone).first()
                if existing_user:
                    flash('Phone number exists.', 'error')
            if existing_user:
                logger.warning(f'Registration error: User exists: {existing_user.id}')
                return redirect(url_for('auth.signup'))

            try:
                # Add new user to the database
                new_user = User(
                    email=email,
                    username=username,
                    phone=phone
                ).set_password(str(password))

                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                # Log database exceptions
                # Send a flash message to the user
                logger.error(f'Signup db exception: {str(e)}')
                flash('Unknown error, please try again.', 'danger')
                return redirect(url_for('auth.signup'))

        except Exception as e:
            # Log database exceptions
            # Send a flash message to the user
            logger.error(f'Signup exception: {str(e)}')
            flash('Unknown error, please try again.', 'danger')
            return redirect(url_for('auth.signup'))

        logger.debug(f'User registered: addr: {request.remote_addr} uid: {new_user.id}')
        # Registration complete, redirect to login
        return redirect(url_for('auth.login'))

    logger.debug(f'Signup request: addr: {request.remote_addr}')
    return render_template('signup.html', form=form)

