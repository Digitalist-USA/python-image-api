"""
A module for handling database ops
"""
from sqlalchemy.sql import select

from database import ENGINE, CAT_RESULTS


def find_cat_result(image_url):
    """
    Fetch a cached is_cat calculation result from database

    Args:
        image_url: url that identifies the cat image

    Returns:
        bool: whether image contains a cat

    """
    sel = select([CAT_RESULTS]).where(CAT_RESULTS.c.image_url == image_url)
    conn = ENGINE.connect()
    try:
        result = conn.execute(sel).first()
        return result['is_cat'] if result is not None else None
    finally:
        conn.close()


def save_cat_result(image_url, is_cat):
    """
    Save a is_cat calculation result in database

    Args:
        image_url: url that identifies the cat image
        is_cat: result of calculation (whether image contains a cat)

    Returns:

    """
    # pylint: disable=no-value-for-parameter
    ins = CAT_RESULTS.insert().values(image_url=image_url, is_cat=is_cat)
    conn = ENGINE.connect()
    try:
        conn.execute(ins)
    finally:
        conn.close()
