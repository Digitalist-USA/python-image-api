"""
Main app is started here
"""
import logging

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

APP = Flask(__name__)

# TODO logging configuration
logging.basicConfig(level="INFO")

# TODO maybe move to a database module
ENGINE = create_engine('sqlite:////tmp/cat.db', convert_unicode=True)
DB_SESSION = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=ENGINE))

# FIXME circular import
# pylint: disable=unused-import
# pylint: disable=wrong-import-position
import endpoints.is_cat


# pylint: disable=unused-argument
@APP.teardown_appcontext
def shutdown_session(exception=None):
    DB_SESSION.remove()
