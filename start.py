"""
Main app is started here
"""
import logging

from flask import Flask

APP = Flask(__name__)

# FIXME circular import
# pylint: disable=unused-import
# pylint: disable=wrong-import-position
import endpoints.is_cat

# TODO logging configuration
logging.basicConfig(level="INFO")
