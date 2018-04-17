"""all common convenience functions live here"""
# pylint: disable=import-error
import os
import re
import logging
import requests
import cv2

LOGGER = logging.getLogger(__name__)


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    Args:
        url:
    Returns:
        bool:
    """
    _head = requests.head(url, allow_redirects=True)
    header = _head.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def get_filename_from_cd(content_desc):
    """
    Get filename from content-disposition
    Args:
        content_desc:
    Returns:
        str:
    """
    if not content_desc:
        return None
    fname = re.findall('filename=(.+)', content_desc)
    if not fname:
        return None
    return fname[0]


def download_image(url, save_path):
    """
    Download an image from URL

    Raises:
        Exceptions for file not downloadable, error file write, error file read.
    Args:
        url: valid image url
        save_path: save to this path

    Returns:
        numpy.ndarray: Image as numpy array
    """
    if not is_downloadable(url=url):
        msg = f'url {url} not downloadable'
        LOGGER.error(msg)
        raise Exception(msg)
    req = requests.get(url, allow_redirects=True)
    filename = get_filename_from_cd(req.headers.get('content-disposition'))
    if filename is None:
        _, ext = os.path.splitext(url)
        filename = f'default{ext}'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filepath = os.path.join(save_path, filename)
    with open(filepath, 'wb') as _file:
        _file.write(req.content)
    if not os.path.exists(filepath):
        msg = f'error writing {filepath} to disk.'
        LOGGER.error(msg)
        raise Exception(msg)
    img = cv2.imread(filepath)
    if img is None:
        msg = f'error reading {filepath} from disk.'
        LOGGER.error(msg)
        raise Exception(msg)
    return img, filepath
