from web.app import create_app
from web.extensions import db, jwt, limiter, oauth, csrf

if __name__ == '__main__':
    """" Run the Flask application """

    # Create the Flask application instance registered with extensions
    app = create_app(db, jwt, limiter, oauth, csrf)

    is_https = app.config['HTTPS_ON']
    port = app.config['SERVER_PORT']
    debug = app.config['DEBUG']

    if is_https:
        # Run the app with SSL context
        app.run(
            port=port,
            debug=debug,
            ssl_context=(
                app.config['HTTPS_CERT'],
                app.config['HTTPS_KEY']
            )
        )
    else:
        app.run(
            port=port,
            debug=debug,
        )
