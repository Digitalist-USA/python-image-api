"""
Example usage of CatImageRec module

"""
from ml.cats import CatImageRec


def print_results(is_cat):
    """
    Print whether cat is in image
    Args:
        is_cat:

    Returns:

    """
    if is_cat:
        print("Image contains cat!")
    else:
        print("Unfortunately, image does not contain cat")


def example_usage():
    """
    Try our CatImageRec on a few example images
    """
    cat_image_rec = CatImageRec()
    cat_image_rec.load_model()
    # pylint: disable=line-too-long
    image_url = 'https://images.pexels.com/photos/20787/pexels-photo.jpg'
    is_cat = cat_image_rec.is_cat(image_url=image_url)
    print_results(is_cat=is_cat)

    image_url = 'http://www.dogbreedslist.info/uploads/allimg/dog-pictures/German-Shepherd-Dog-1.jpg'
    is_cat = cat_image_rec.is_cat(image_url=image_url)
    print_results(is_cat=is_cat)

    image_url = 'http://r.ddmcdn.com/s_f/o_1/cx_462/cy_245/cw_1349/ch_1349/w_720/APL/uploads/2015/06/caturday-shutterstock_149320799.jpg'
    is_cat = cat_image_rec.is_cat(image_url=image_url)
    print_results(is_cat=is_cat)


if __name__ == '__main__':
    example_usage()
