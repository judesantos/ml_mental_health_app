from web.app import create_app
from web.extensions import db, jwt, limiter, oauth, csrf


if __name__ == '__main__':
    """" Run the Flask application """
    # Create the Flask application instance registered with extensions
    app = create_app(db, jwt, limiter, oauth, csrf)
    # Run the app with SSL context
    app.run(
        debug=True,
        ssl_context=(
            'certs/app_certificate.pem',
            'certs/app_private_key.pem'
        )
    )
