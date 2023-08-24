# Flask modules
from flask import current_app
from flask.wrappers import Request, Response

# Local modules
from app.extensions import cache


def make_api_cache_key(request: Request):
    full_url = request.url
    return full_url.split("/api/")[-1]


def is_exempted_route(route_path: str):
    return any(
        (
            route_path.startswith(x)
            for x in current_app.config["CACHE_EXEMPTED_ROUTES"]
        )
    )


def get_cached_response(request: Request):
    if not current_app.config['CACHE_ENABLED'] or is_exempted_route(request.path):
        return None

    cache_key = make_api_cache_key(request)
    try:
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return cached_response
    except Exception as e:
        print("Error when fetching cached response:", e)

    return None


def set_cached_response(request: Request, response: Response):
    if not current_app.config['CACHE_ENABLED'] or is_exempted_route(request.path):
        return None

    try:
        cache_key = make_api_cache_key(request)
        if not cache.get(cache_key):
            cache.set(cache_key, response)
    except Exception as e:
        print("Error when caching response:", e)

    return None
