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
from flask_jwt_extended import get_jwt_identity
from flask_login import login_user, logout_user, current_user

from extensions import db, oauth, limiter
from settings import settings
from models.user import User

from ui.forms.signup_form import SignupForm
from ui.forms.login_form import LoginForm

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
@limiter.limit("5 per minute")
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
@limiter.limit("5 per minute")
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


@bp.route('/protected', methods=['GET'])
@limiter.limit("5 per minute")
@jwt_required()
def protected():
    """
    This is an example endpoint that requires a valid access token to access.
    """
    current_user = get_jwt_identity()
    return jsonify({
        "message": f"Welcome {current_user}, you have accessed a protected \
        route!"
    }), 200


@bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """
    Registers a new user with the provided username, password, and email.
    The username, password, and email are required parameters in the
    request body.
    Saves the user information to the database.

    Returns:
        400: If the username, password, or email are missing, or if the email
            is already registered.
        201: If the user is registered successfully.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({
            "message": "Username, password, and email are required"
        }), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
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
                user = User.query.filter_by(email=username).first()
            if user:
                if user.check_password(password=password):
                    session['user_id'] = user.id
                    # Validation successful, create access token and
                    # redirect to the dashboard
                else:
                    validation_success = False
            else:
                validation_success = False

            if validation_success is False:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('auth.login'))

        except Exception as e:
            print(f'Database exception: {str(e.with_traceback(None))}')
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

        print('Login Success. Redirect to dashboard')
        return response

    return render_template('login.html', form=form)


@bp.route('/logout', methods=['get'])
@limiter.limit("10 per minute")
@jwt_required()
def logout():
    """
    Logout the currently authenticated user.
    The access token is invalidated by removing the JWT cookies.

    Redirects to the home page after logout.
    """

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

    return redirect(url_for('main.home'))


@bp.route('/signup', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
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
                print('User exists')
                return redirect(url_for('auth.signup'))

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
            print(f'DB Exception: {str(e)}')
            # Send a flash message to the user
            flash(
                'Server encountered a problem, please try again.',
                category='danger'
            )
            flash('Unknown error, please try again.', 'danger')
            return redirect(url_for('auth.login'))

        # Registration complete, redirect to login
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)


@bp.route('/error')
@limiter.limit("2 per minute")
def error():
    """
    Display a custom error message when login fails.
    """
    return render_template('error.html')
