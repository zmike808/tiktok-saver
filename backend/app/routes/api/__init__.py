# Flask modules
from flask import Blueprint
from werkzeug.exceptions import HTTPException
from flask_limiter.errors import RateLimitExceeded

# Local modules
from app.extensions import cache, limiter
from app.utils.api import error_response, make_cache_key, get_cached_response

# Blueprint modules
from app.routes.api.tests import tests_bp
from app.routes.api.proxy import proxy_bp
from app.routes.api.tiktok import tiktok_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, RateLimitExceeded):
        current_limit = error.limit.limit
        return error_response(f"Too many requests: {current_limit}", 429)
    elif isinstance(error, HTTPException):
        return error_response(error.description, error.code)
    else:
        print(error)
        return error_response()


@api_bp.before_request
def before_request():
    # Check if user is rate limited
    current_limit = limiter.current_limit
    if current_limit:
        if current_limit.remaining <= 0:
            return

    # Attempt to fetch cached response
    cache_key = make_cache_key()
    try:
        cached_response = get_cached_response(cache_key)
        if cached_response is not None:
            return cached_response
    except Exception as e:
        print(f"Error when fetching cached response:", e)


@api_bp.after_request
def after_request(response):
    if response.status_code == 200:
        # Cache the response if it is successful (status code 200)
        try:
            cache_key = make_cache_key()
            cache.set(cache_key, response, timeout=300)
        except Exception as e:
            print(f"Error when caching response:", e)
    return response


api_bp.register_blueprint(tests_bp)
api_bp.register_blueprint(proxy_bp)
api_bp.register_blueprint(tiktok_bp)