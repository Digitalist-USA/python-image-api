"""
/is_cat endpoint
"""
import logging

from flask import jsonify, request

from start import APP
from service.cat_service import CAT_SERVICE


LOGGER = logging.getLogger(__name__)


@APP.route("/is_cat", methods=["GET", "POST"])
def is_cat():
    """
    Main API endpoint

    Following query parameter are defined:

        image_url: (required) valid url to image
        nocache: (optional) if provided, do not check cache for is_cat results

    Returns:
    """
    try:
        image_url = request.args["image_url"]
    except KeyError:
        msg = "Missing required query parameter: image_url"
        LOGGER.warning(msg)
        return jsonify({"status": 400, "message": msg}), 400
    # GET
    if request.method == "GET":
        use_cache = True if request.args.get("nocache") is None else False
        result = CAT_SERVICE.is_cat(image_url, use_cache)  # FIXME first check url?
        return jsonify({"status": 200, "message": result})
    # POST
    CAT_SERVICE.save_cat(image_url)
    return jsonify({"status": 200, "message": "OK"})  # for now


@APP.errorhandler(404)
def not_found(error):
    """
    Custom error handling (404)

    Args:
    Returns:
    """
    LOGGER.warning(error)
    return jsonify({"status": 404, "message": "Not found"}), 404


@APP.errorhandler(405)
def not_allowed(error):
    """
    Custom error handling (405)

    Args:
    Returns:
    """
    LOGGER.warning(error)
    return jsonify({"status": 405, "message": "Method not allowed"}), 405


@APP.errorhandler(500)
def server_error(error):
    """
    Custom error handling (500)

    Args:
    Returns:
    """
    LOGGER.error("Unexpected exception: %s", error)
    return jsonify({"status": 500, "message": "Server error"}), 500
