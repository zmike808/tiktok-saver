# Flask modules
from flask import Blueprint, request, abort
from werkzeug.exceptions import BadRequest, InternalServerError, Forbidden

# Local modules
from app.models.test import TestModel
from app.utils.api import success_response
from app.extensions import limiter

tests_bp = Blueprint("tests", __name__, url_prefix="/tests")


@tests_bp.before_request
def limit_tests_access():
    allowed_hosts = ("127.0.0.1", "::1", "localhost")
    if request.remote_addr not in allowed_hosts:
        abort(403)


@tests_bp.route("/success", methods=["GET"])
def test_api_success():
    data = TestModel(title="riad-azz", content="Successful API response")
    return success_response(data, 200)


@tests_bp.route("/ratelimit", methods=["GET"])
@limiter.limit("1 per minute", override_defaults=True)
def test_api_ratelimit():
    data = TestModel(title="riad-azz", content="Rate limit API response")
    return success_response(data, 200)


@tests_bp.route("/cached", methods=["GET"])
def test_api_cached():
    data = TestModel(title="riad-azz", content="Cached API response")
    return success_response(data, 200)


@tests_bp.route("/bad-request", methods=["GET"])
def test_api_bad_request():
    raise BadRequest("Bad Request")


@tests_bp.route("/forbidden", methods=["GET"])
def test_api_forbidden():
    raise Forbidden("You don't have the permission to access the requested resource")


@tests_bp.route("/internal-server-error", methods=["GET"])
def test_api_internal_server_error():
    raise InternalServerError("Internal Server Error")


@tests_bp.route("/unknown-exception", methods=["GET"])
def test_api_unknown_error():
    raise Exception("Unknown Exception")
