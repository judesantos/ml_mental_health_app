
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from flask_limiter.util import get_remote_address
from flask_login import LoginManager

# Initialize plugins

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
oauth = OAuth()
csrf = CSRFProtect()
login_manager = LoginManager()
