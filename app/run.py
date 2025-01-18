from app import create_app
from extensions import db, jwt, limiter, oauth, csrf

# Create the Flask application instance registered with extensions
app = create_app(db, jwt, limiter, oauth, csrf)

if __name__ == '__main__':
    """" Run the Flask application """

    # Run the app with SSL context
    app.run(
        debug=True,
        ssl_context=(
            'certs/app_certificate.pem',
            'certs/app_private_key.pem'
        )
    )
