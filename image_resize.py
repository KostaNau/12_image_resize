import argparse
import textwrap
from os import path

from PIL import Image


def get_parser():
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent('''\
                    *** SIMPLE IMAGE RESIZER TOOL ***
            -------------------------------------------------------------------
            |   Image resizer tool is a useful script for quick resize jpg,   |
            |   png, bmp, pcx, tiff images formats. Helpful for front-end     |
            |   web-developers.                                               |
            -------------------------------------------------------------------
                    '''))
    parser.add_argument('target',
                        help="path to the image")
    parser.add_argument('-width', '--width',
                        type=int,
                        default=None,
                        help="width result image")
    parser.add_argument('-heigth', '--heigth',
                        type=int,
                        default=None,
                        help="heigth result image")
    parser.add_argument('-scale', '--scale',
                        type=float,
                        default=None,
                        help="scale result image")
    parser.add_argument('-destination', '--destination',
                        default=None,
                        help="path for save result image")
    return parser


def open_initial_image(path_to_image: str):
    try:
        image = Image.open(path_to_image)
    except IOError:
        pass
    return image


def get_aspect_ratio(image):
    width, heigth = image.size   # 2-tuple containing width and height
    return round(width / heigth, 2)


def linear_size_change(image, user_width, user_heigth):
    original_ratio = get_aspect_ratio(image)
    if user_width and user_heigth:
        resize_image = image.resize((user_width, user_heigth))
        if original_ratio != get_aspect_ratio(resize_image):
            print('Warning, your resized image has a wrong ratio!')
    elif user_width:
        adjusted_heigth = int(user_width * original_ratio)
        resize_image = image.resize((user_width, adjusted_heigth))
    elif user_heigth:
        adjusted_width = int(user_heigth * original_ratio)
        resize_image = image.resize((adjusted_width, user_heigth))
    return resize_image


def change_by_scale(image, scale):
    width, heigth = image.size
    adjusted_width, adhusted_heigth = int(width * scale), int(heigth * scale)
    resize_image = image.resize((adjusted_width, adhusted_heigth))
    return resize_image


def resize_image(image, options):
    if options.scale and (options.width or options.heigth):
        raise TypeError('Incorrect. Either scale or height and width options')
    elif options.scale:
        return change_by_scale(image, options.scale)
    elif options.width or options.heigth:
        return linear_size_change(image, options.width, options.heigth)


def save_resized_image(resize_image, options):
    base = path.basename(options.target)
    original_name = path.splitext(base)[0]
    extension = path.splitext(base)[1].lower()
    if options.destination:
        resize_image.save(
            '{0}{1}_{2}x{3}{4}'.format(
                                        options.destination,
                                        original_name,
                                        *resize_image.size,
                                        extension))
    resize_image.save('{0}_{1}x{2}{3}'.format(
                                              original_name,
                                              *resize_image.size,
                                              extension))


if __name__ == '__main__':
    options = get_parser().parse_args()
    original_image = open_initial_image(options.target)
    new_image = resize_image(original_image, options)
    save_resized_image(new_image, options)
