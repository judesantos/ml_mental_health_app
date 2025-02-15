from app.web.app import create_app
from app.web.extensions import db, jwt, limiter, oauth, csrf

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Create the Flask application instance registered with extensions
app = create_app(db, jwt, limiter, oauth, csrf)

if __name__ == '__main__':
    """" Run the Flask application """
    # Run the app with SSL context
    app.run(
        host=app.config.get('SERVER_NAME'),
        port=app.config.get('SERVER_PORT'),
        debug=app.config.get('DEBUG'),
        ssl_context=(
            'certs/app_certificate.pem',
            'certs/app_private_key.pem'
        )
    )
