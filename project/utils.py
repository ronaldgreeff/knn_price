import colorsys
import json

def str_px_to_float(string_px):
    """ turn px input (str, int or float) to float """
    if type(string_px) == type(str()):
        if string_px[-2:] == 'px':
            string_px = string_px[:-2]

    return float(string_px)


def is_it_color(rgb_string, sat_thr=0.19, val_thr_b=0.11, val_thr_u=1.0):
    """ Determine if rgb value is "colourful" or not.
    Convert rgb to hsv model to make less complex:
        hue: ignored (actual colour doesn't matter)
        val: black (low) to white (high) lightness
        sat: dull (low) to intense (high) colour
    val can't be too light or too dark / must be within extremes
    sat must be higher than threshold to be considered coloured
    Return 0 or 1 so that we get large separation between datapoints if coloured
    """
    r, g, b = rgb_to_coords(rgb_string)
    hue, sat, val = colorsys.rgb_to_hsv(r, g, b)

    eval_extremes = (val_thr_b < val <= val_thr_u)
    eval_intensity = (sat_thr < sat)

    eval = 1 if all((eval_extremes, eval_intensity,)) else 0

    # print(
    # 'sat: {} sat_thr: {} *{}| val: {} val-b: {} val-u: {} *{} | *{}*\n'.format(
    # sat, sat_thr, eval_intensity, val, val_thr_b, val_thr_u, eval_extremes, eval)
    # )

    return eval


def rgb_to_coords(rgb_string):
    """ Remove 'rgb' from rgb_string, split num_str ["r", "g", "b"]
    convert each num_str to int and
    divide by 255 so that coordinates are between 0 - 1 (YIQ space)
    """
    return [ (int(num_str)/255) for num_str in rgb_string[4:-1].split(',') ]


def text_to_features(texts):
    """
    Params: a list of strings (texts)
    Output: len, chars, digits, spaces, denom for joined texts
    """
    len = 0
    chars = 0
    digits = 0
    spaces = 0
    denom = 0

    texts = json.loads(texts)
    text = ''.join(texts)

    for t in text:
        if t.isalpha():
            chars += 1
        elif t.isdigit():
            digits += 1
        elif t.isspace():
            spaces += 1
        else:
            if t in ('£', '$'):
                denom += 1
        len += 1

    return  text, len, digits, chars, spaces, denom
