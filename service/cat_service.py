"""
A service layer module for cat image recognition
"""
from ml.cats import CatImageRec


class CatService:
    """
    Cat recognition service
    """

    def __init__(self):
        self.cat_image_rec = CatImageRec()
        self.cat_image_rec.load_model()

    def is_cat(self, url):
        """
        Predicts whether image contains a cat

        TODO: will check database first

        Args:
            url: valid url to image

        Returns:
            bool: whether image is a cat
        """
        return self.cat_image_rec.is_cat(image_url=url)

    def save_cat(self, url):
        """
        Predicts whether image contains a cat and saves result in database
        Args:
            url: valid url to image

        Returns: ???

        """
        pass


CAT_SERVICE = CatService()
