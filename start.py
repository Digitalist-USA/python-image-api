"""
Main app is started here
"""
import logging

from flask import Flask

APP = Flask(__name__)

logging.basicConfig(level="INFO")

# pylint: disable=unused-import
# pylint: disable=wrong-import-position
import endpoints.is_cat
