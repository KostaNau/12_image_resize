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
    parser.add_argument('--width',
                        type=int,
                        default=None,
                        help="width result image")
    parser.add_argument('--heigth',
                        type=int,
                        default=None,
                        help="heigth result image")
    parser.add_argument('--scale',
                        type=float,
                        default=None,
                        help="scale result image")
    parser.add_argument('--destination',
                        default=None,
                        help="path for save result image")
    return parser


def open_initial_image(path_to_image: str):
    try:
        image = Image.open(path_to_image)
    except IOError:
        pass
    return image


def resize_image_sides(image, width, heigth):
    return image.resize((width, heigth))


def get_aspect_ratio(image):
    width, heigth = image.size
    return round(width / heigth, 2)


def initialize_filename(image, **options):
    base = path.basename(options['original_path'])
    original_name = path.splitext(base)[0]
    print(original_name)
    extension = path.splitext(base)[1].lower()
    if options['destination']:
        name = options['destination'], original_name, *image.size, extension
    else:
        name = original_name, *image.size, extension
    filename = '{}_{}x{}{}'.format(*name)
    return filename


def resize_linear(image, user_width, user_heigth):
    original_ratio = get_aspect_ratio(image)
    if user_width and user_heigth:
        resized_image = resize_image_sides(image,
                                           user_width,
                                           user_heigth
                                           )
        if original_ratio != get_aspect_ratio(resized_image):
            print('Warning, your resized image has a wrong ratio!')
    elif user_width:
        adjusted_heigth = int(user_width * original_ratio)
        resized_image = resize_image_sides(image,
                                           user_width,
                                           adjusted_heigth
                                           )
    elif user_heigth:
        adjusted_width = int(user_heigth * original_ratio)
        resized_image = resize_image_sides(image,
                                           adjusted_width,
                                           user_heigth
                                           )
    return resized_image


def resize_scale(image, scale):
    width, heigth = image.size
    adjusted_width, adjusted_heigth = int(width * scale), int(heigth * scale)
    resized_image = resize_image_sides(image,
                                       adjusted_width,
                                       adjusted_heigth
                                       )
    return resized_image


def resize_new_image(image, **options):
    if options['scale'] and (options['width'] or options['heigth']):
        raise TypeError('Incorrect. Either scale or height and width options')
    elif options['scale']:
        return resize_scale(image, options['scale'])
    elif options['width'] or options['heigth']:
        return resize_linear(image, options['width'], options['heigth'])


if __name__ == '__main__':
    options = get_parser().parse_args()
    original_image = open_initial_image(options.target)
    new_image = resize_new_image(original_image,
                                 width=options.width,
                                 heigth=options.heigth,
                                 scale=options.scale
                                 )
    filename = initialize_filename(new_image,
                                   original_path=options.target,
                                   destination=options.destination,
                                   )
    new_image.save(filename)
