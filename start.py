"""
Main app is started here
"""
import logging

from flask import Flask
from sqlalchemy import create_engine, MetaData, Table, Column, Boolean, String

APP = Flask(__name__)

# TODO logging configuration
logging.basicConfig(level="INFO")

# TODO maybe move to a database module
ENGINE = create_engine('sqlite:////tmp/cat.db', convert_unicode=True, echo=True)

METADATA = MetaData(bind=ENGINE)
# Create DB tables here (for now)
CAT_RESULTS = Table('cat_results', METADATA,
                    Column('image_url', String, primary_key=True),
                    Column('is_cat', Boolean), )

METADATA.create_all(ENGINE)

# FIXME circular import
# pylint: disable=unused-import
# pylint: disable=wrong-import-position
import endpoints.is_cat
