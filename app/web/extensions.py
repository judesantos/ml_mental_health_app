
"""
This module contains the initialization of the
Flask extensions used in the application.
Caching service is also provded bt this module.

Functions:
    cache_push: Cache the data in the in-memory cache.
    cache_get: Retrieve the data from the in-memory
        cache but do not remove it from cache.
    cache_pop: Retrieve the data from the in-memory
        cache and remove it from cache.

Properties:
    db: SQLAlchemy object
    jwt: JWTManager object
    limiter: Limiter object
    oauth: OAuth object
    csrf: CSRFProtect object
    login_manager: LoginManager object
    CACHE_TTL: int
    CACHE_MAXSIZE: int
    ttl_cache: TTLCache object
"""

import uuid
# TODO: Use redis for caching in production
from cachetools import TTLCache

from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from flask_limiter.util import get_remote_address
from flask_login import LoginManager

# 1. Initialize Flask plugins

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
oauth = OAuth()
csrf = CSRFProtect()
login_manager = LoginManager()


# 2. Implement application caching service

# In-memory cache settings

CACHE_TTL = 60 * 30  # 30 minutes
CACHE_MAXSIZE = 1000
ttl_cache = TTLCache(maxsize=CACHE_MAXSIZE, ttl=CACHE_TTL)


def cache_push(data: dict) -> str:
    """
    Cache the data in the in-memory cache.

    Args:
        data (dict): The data to be cached.
    Returns:
        str: The key to retrieve the data from the cache.
    """
    key = str(uuid.uuid4())
    ttl_cache[key] = data
    return key


def cache_get(key: str) -> dict:
    """
    Retrieve the data from the in-memory cache but do not remove it from cache.

    Args:
        key (str): The key to retrieve the data from the cache.
    Returns:
        dict: The data from the cache.
    """
    if key not in ttl_cache:
        return None
    return ttl_cache[key]


def cache_pop(key: str) -> dict:
    """
    Retrieve the data from the in-memory cache and remove it from cache.

    Args:
        key (str): The key to retrieve the data from the cache.
    Returns:
        dict: The data from the cache.
    """
    if key not in ttl_cache:
        return None
    return ttl_cache.pop(key)
