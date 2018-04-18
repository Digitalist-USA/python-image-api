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

    Request must contain the following query parameter:

        image_url: valid url to image

    Returns:
    """
    if request.method == "GET":
        try:
            url = request.args["image_url"]
        except KeyError:
            msg = "Missing required query parameter: image_url"
            LOGGER.warning(msg)
            return jsonify({"status": 400, "message": msg}), 400
        result = CAT_SERVICE.is_cat(url)  # FIXME first check url?
        return jsonify({"status": 200, "message": result})
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
