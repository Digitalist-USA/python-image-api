"""
A module for handling database ops
"""
import datetime

from collections import namedtuple

from sqlalchemy.sql import select

from database import ENGINE, CAT_RESULTS


CatResult = namedtuple("CatResult", ["image_url", "is_cat", "created", "last_modified"])


def find_cat_result(image_url):
    """
    Fetch a cached is_cat calculation result from database

    Args:
        image_url: url that identifies the image

    Returns:
        tuple: (str, bool, float, float)

    """
    sel = select([CAT_RESULTS]).where(CAT_RESULTS.c.image_url == image_url)
    conn = ENGINE.connect()
    try:
        result = conn.execute(sel).first()
        if result is None:
            return result
        # pylint: disable=line-too-long
        return CatResult(result["image_url"], result["is_cat"], result["created"], result["last_modified"])
    finally:
        conn.close()


def insert_cat_result(image_url, is_cat):
    """
    Save an is_cat calculation result in database

    Args:
        image_url: url that identifies the image
        is_cat: result of calculation (whether image contains a cat)

    Returns:

    """
    # pylint: disable=no-value-for-parameter
    now = datetime.datetime.now().timestamp()
    ins = CAT_RESULTS.insert().\
        values(image_url=image_url, is_cat=is_cat, created=now, last_modified=now)
    conn = ENGINE.connect()
    try:
        conn.execute(ins)
    finally:
        conn.close()


def update_cat_result(image_url, is_cat):
    """
    Update an is_cat calculation result in database

    Args:
        image_url: url that identifies the image
        is_cat: result of calculation (whether image contains a cat)

    Returns:

    """
    # pylint: disable=no-value-for-parameter
    now = datetime.datetime.now().timestamp()
    upd = CAT_RESULTS.update().\
        where(CAT_RESULTS.c.image_url == image_url).\
        values(is_cat=is_cat, last_modified=now)
    conn = ENGINE.connect()
    try:
        conn.execute(upd)
    finally:
        conn.close()
