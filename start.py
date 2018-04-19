"""
Main app is started here
"""
import logging

from flask import Flask
from sqlalchemy import create_engine

APP = Flask(__name__)

# TODO logging configuration
logging.basicConfig(level="INFO")

# TODO maybe move to a database module
ENGINE = create_engine('sqlite:////tmp/cat.db', convert_unicode=True)

# FIXME circular import
# pylint: disable=unused-import
# pylint: disable=wrong-import-position
import endpoints.is_cat
