"""
Celery tasks
"""
import logging

from celery import Celery

from service.cat_service import CAT_SERVICE


LOGGER = logging.getLogger(__name__)


CELERY_APP = Celery("tasks", broker="redis://localhost:6379/0")

CELERY_APP.conf.broker_transport_options = {"visibility_timeout": 300}  # seconds
CELERY_APP.conf.task_serializer = "json"  # default


@CELERY_APP.task
def process_and_save(image_url):
    """
    Process an image and save results, task-ified

    Args:
        image_url: valid url to image

    Returns:
        str:
    """
    try:
        CAT_SERVICE.save_cat(image_url)
        return f"Successfully processed {image_url}"
    # pylint: disable=broad-except
    except Exception as ex:
        LOGGER.exception(ex)
        return f"Failed to process {image_url}"
