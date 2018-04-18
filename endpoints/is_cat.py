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
    else:
        LOGGER.warning("Request method %s unimplemented", request.method)
        return jsonify({"status": 405, "message": "Unimplemented method"}), 405
