"""
Cat Image Recognition module
"""
from common.util import download_image
from ml.model.inception_v3_imagenet import InceptionV3
import ml.config as cfg


class CatImageRec(object):
    """
    Cat Image Recognition
    """

    def __init__(self):
        self.model = None

    def load_model(self):
        """
        Load Model

        """
        self.model = InceptionV3()

    @staticmethod
    def string_contains_cat(string: str) -> bool:
        """
        Determine whether string contains cat
        Args:
            string:

        Returns:
            bool: whether string contains cat

        """
        words = string.split()
        words_lower = [word.lower() for word in words]
        if 'cat' in words_lower:
            return True
        return False

    def is_cat(self, image_url: str) -> bool:
        """
        Predict whether image contains a cat
        Args:
            image_url: valid url to image.
        Warnings:
            Due to lazy url parsing in download_image(),
            image_url must end in image filename with extension
            (eg. website.com/image.jpg NOT website.com/image.jpg?dim=300x300)

        Returns:

        """
        _, img_filename = download_image(url=image_url, save_path=cfg.IMAGE_SAVE_DIR)
        predictions = self.model.predict(image_file=img_filename, num_top_predictions=5)
        for pred in predictions:
            cls = pred['class']
            if self.string_contains_cat(string=cls):
                return True
        return False
