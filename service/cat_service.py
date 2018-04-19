"""
A service layer module for cat image recognition
"""
import logging

from ml.cats import CatImageRec

from .cat_repository import find_cat_result, save_cat_result


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
            LOGGER.info("Checking cache for %s", image_url)
            result = find_cat_result(image_url)
            if result is not None:
                LOGGER.info(
                    "Found result in cache: %s %s a cat", image_url, "is" if result else "is not"
                )
                return result
            else:
                LOGGER.info("%s not found in cache", image_url)
        return self.cat_image_rec.is_cat(image_url=image_url)

    def save_cat(self, image_url):
        """
        Predicts whether image contains a cat and saves result in database

        TODO: use task queue to compute result later

        Args:
            image_url: valid url to image

        Returns:

        """
        result = self.cat_image_rec.is_cat(image_url)
        save_cat_result(image_url, result)


CAT_SERVICE = CatService()
