"""

"""

import datetime

from flask import url_for, jsonify
from flask import Flask, request, redirect
from flask_talisman import Talisman
from flask_login import current_user

from web.routes import main, auth
from web.settings import settings
from web.extensions import jwt, login_manager, limiter
from web.models.user import User

from loguru import logger
from ml.config.logging import configure_logging


def init_app_configs(app):
    """
    Initialize the application configurations.

    This function sets up the application configurations using the
    settings module.

    Args:
        app (Flask): The Flask application instance.
    """

    configure_logging()

    track_notifications = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    google_discovery_url = settings.GOOGLE_DISCOVERY_URL

    app.config['ENV'] = settings.ENV
    app.config['DEBUG'] = settings.DEBUG

    app.config['SERVER_NAME'] = settings.SERVER_NAME
    app.config['SERVER_PORT'] = settings.SERVER_PORT

    app.config['SESSION_COOKIE_DOMAIN'] = False
    app.config['SERVER_NAME'] = settings.SERVER_NAME

    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    app.config['JWT_COOKIE_SECURE'] = settings.JWT_COOKIE_SECURE
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    # Disable CSRF protection for now
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_COOKIE_SAMESITE'] = 'Strict'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)

    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = track_notifications

    app.config['GOOGLE_CLIENT_ID'] = settings.GOOGLE_CLIENT_ID
    app.config['GOOGLE_CLIENT_SECRET'] = settings.GOOGLE_CLIENT_SECRET
    app.config['GOOGLE_DISCOVERY_URL'] = google_discovery_url
    app.config['MAX_CONTENT_LENGTH'] = settings.MAX_CONTENT_LENGTH

    app.debug = True


def init_middleware_callbacks(app, failback_page='auth.home'):
    """
    Initialize the application middleware callbacks.

    This function sets up the application middleware callbacks for
    handling expired, invalid, and unauthorized JWT tokens.

    Args:
        app (Flask): The Flask application instance.
    """

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return redirect(url_for(failback_page))

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return redirect(url_for(failback_page))

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return redirect(url_for(failback_page))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    @app.before_request
    def redirect_to_https():
        # Redirect to HTTPS if not in development mode
        if not request.is_secure and app.env != "development":
            return redirect(request.url.replace("http://", "https://"))

    @app.route('/debug')
    @limiter.limit("100 per minute")
    def debug():
        if current_user.is_authenticated:
            user_info = f'Current user: {current_user}'
            logger.debug(f'/debug: User is authenticated: {user_info}')
            return jsonify(
                {"message": "User is authenticated",
                 "user": str(current_user)}
            ), 200
        else:
            logger.debug('/debug: No user is authenticated')
            return jsonify(
                {"message": "No user is currently authenticated"}
            ), 200


def create_app(db, jwt, limiter, oauth, csrf):
    """
    Create the Flask application instance.

    This function creates the Flask application instance and initializes
    the application configurations and middleware callbacks.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
        jwt (JWTManager): The JWT manager instance.
        limiter (Limiter): The rate limiter instance.
        oauth (OAuth): The OAuth instance.
        csrf (CSRFProtect): The CSRF protection instance.
    """

    logger.info('Starting create_app...')

    app = Flask(__name__)

    # Secure headers
    csp = {
        'default-src': ["'self'"],
        'img-src': ["'self'", "data:"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'script-src': ["'self'", "'unsafe-inline'"],
        #    'img-src': ["'self'", "https://trusted.cdn.com"]
    }
    Talisman(app, content_security_policy=csp)

    # Configure app
    init_app_configs(app)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)
    oauth.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    with app.app_context():
        db.create_all()

    init_middleware_callbacks(app, failback_page='main.home')

    return app
