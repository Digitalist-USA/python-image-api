"""
/is_cat endpoint
"""
import logging

from flask import jsonify, request

from common.util import is_downloadable
from service.cat_service import CAT_SERVICE
from start import APP
from tasks import process_and_save


LOGGER = logging.getLogger(__name__)


@APP.route("/is_cat", methods=["GET", "POST"])
def is_cat():
    """
    Main API endpoint

    Following query parameters are defined:

        image_url: (required) valid url to image
        nocache: (optional) if provided, do not check cache for is_cat results

    Returns:
    """
    try:
        image_url = request.args["image_url"]
    except KeyError:
        msg = "Missing required query parameter: image_url"
        LOGGER.warning(msg)
        return jsonify({"status": 400, "result": None, "message": msg}), 400
    if not is_downloadable(image_url):
        msg = "Bad parameter: image_url is not downloadable"
        LOGGER.warning(msg)
        return jsonify({"status": 400, "result": None, "message": msg}), 400
    # GET
    if request.method == "GET":
        use_cache = True if request.args.get("nocache") is None else False
        result = CAT_SERVICE.is_cat(image_url, use_cache)
        msg = f"Image contains {'no' if not result else 'a'} cat"
        return jsonify({"status": 200, "result": result, "message": msg})
    # POST
    process_and_save.delay(image_url)
    return jsonify({"status": 202, "result": None, "message": "Accepted"})


@APP.errorhandler(404)
def not_found(error):
    """
    Custom error handling (404)

    Args:
    Returns:
    """
    LOGGER.warning(error)
    return jsonify({"status": 404, "result": None, "message": "Not found"}), 404


@APP.errorhandler(405)
def not_allowed(error):
    """
    Custom error handling (405)

    Args:
    Returns:
    """
    LOGGER.warning(error)
    return jsonify({"status": 405, "result": None, "message": "Method not allowed"}), 405


@APP.errorhandler(500)
def server_error(error):
    """
    Custom error handling (500)

    Args:
    Returns:
    """
    LOGGER.error("Unexpected exception: %s", error)
    return jsonify({"status": 500, "result": None, "message": "Server error"}), 500
