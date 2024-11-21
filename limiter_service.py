from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_app import app
from os import getenv

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=getenv('RATELIMIT_STORAGE_URL', 'memory://')
)