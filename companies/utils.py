import os

from colormap import rgb2hex


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.pk, ext)
    return os.path.join('company_logos', filename)


def get_color(colors):
    brightest_color = None
    max_brightness = -1
    white_brightness = 0.299 * 255 + 0.587 * 255 + 0.114 * 255

    for (r, g, b), percent in colors:
        # Calculate brightness using the formula: 0.299*R + 0.587*G + 0.114*B
        brightness = 0.299 * r + 0.587 * g + 0.114 * b

        # Exclude white color and find the brightest color
        if not brightness == white_brightness and max_brightness < brightness:
            max_brightness = brightness
            brightest_color = rgb2hex(int(r), int(g), int(b))

    return brightest_color or '#57B223'
