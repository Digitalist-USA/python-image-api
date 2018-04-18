"""
/is_cat endpoint
"""
import logging

from flask import jsonify, request

from start import APP


LOGGER = logging.getLogger(__name__)


@APP.route("/is_cat", methods=["GET", "POST"])
def is_cat():
    if request.method == "GET":
        LOGGER.info("Received a GET request")
        return jsonify({"status": 200, "message": "OK"})
    LOGGER.warning("Request method %s unimplemented", request.method)
    return jsonify({"status": 405, "message": "Unimplemented method"}), 405


@APP.errorhandler(404)
def not_found(error):
    """
    Custom error handling (404)

    Args:
    Returns:
    """
    LOGGER.warning(error)
    return jsonify({"status": 404, "message": "Not found"}), 404


@APP.errorhandler(500)
def server_error(error):
    """
    Custom error handling (500)

    Args:
    Returns:
    """
    LOGGER.error("Unexpected exception: %s", error)
    return jsonify({"status": 500, "message": "Server error"}), 500
