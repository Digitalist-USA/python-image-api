"""
A service layer module for cat image recognition
"""
import logging

from ml.cats import CatImageRec

from .cat_repository import find_cat_result, insert_cat_result, update_cat_result


LOGGER = logging.getLogger(__name__)


class CatService:
    """
    Cat recognition service
    """

    def __init__(self):
        self.cat_image_rec = CatImageRec()
        self.cat_image_rec.load_model()

    def is_cat(self, image_url, use_cache):
        """
        Predicts whether image contains a cat

        Args:
            image_url: valid url to image
            use_cache: whether to check cache for results first

        Returns:
            bool: whether image contains a cat
        """
        if use_cache:
            LOGGER.info(f"Checking cache for {image_url}")
            result = find_cat_result(image_url)
            if result is not None:
                _is_cat = "is" if result.is_cat else "is not"
                LOGGER.info(f"Found result in cache: {image_url} {_is_cat} a cat")
                return result.is_cat
            else:
                LOGGER.info(f"{image_url} not found in cache")
        return self.cat_image_rec.is_cat(image_url=image_url)

    def save_cat(self, image_url):
        """
        Predicts whether image contains a cat and saves result in database

        Args:
            image_url: valid url to image

        Returns:

        """
        result = self.cat_image_rec.is_cat(image_url)
        # check if results have been previously cached; update if necessary
        cached = find_cat_result(image_url)
        if cached is None:
            LOGGER.info(f"Saving new results for {image_url}")
            insert_cat_result(image_url, result)
        else:
            if cached.is_cat != result:
                LOGGER.info(f"Updating previously stored results for {image_url}")
                update_cat_result(image_url, result)
            else:
                LOGGER.info(f"No change to results for {image_url}")


CAT_SERVICE = CatService()
