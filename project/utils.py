import colorsys

def str_px_to_float(string_px):
    """ turn px input (str, int or float) to float """
    if type(string_px) == type(str()):
        if string_px[-2:] == 'px':
            string_px = string_px[:-2]
    return float(string_px)

def is_it_color(rgb_string, sat_thr=0.2, val_thr_b=0.1, val_thr_u=1):
    """ Determine if rgb value is "colourful" or not.
    Convert rgb to hsv model to make less complex:
        hue: ignored (actual colour doesn't matter)
        sat: dull (low) to intense (high) colour
        val: black (low) to white (high) lightness
    If val falls between val bottom and upper thresholds, its
    considered "potentially colourful" (since not too light or dark).
    If it's sat/colour intensity above given threshold, it's considered coloured
    Return 0 or 1 so that we get large separation between datapoints if coloured
    """

    r, g, b = rgb_to_coords(rgb_string)
    hue, sat, val = colorsys.rgb_to_hsv(r, g, b)

    val = (val_thr_b < val < val_thr_u)
    sat = (val > sat_thr)
    eval = 1 if all((val, sat,)) else 0

    print(val, sat, eval)

    #       sat too dull or val below bottom or val above upper
    # eval = (sat < sat_thr or val_thr_b > val or val > val_thr_u)
    # result = 0 if eval else 1

    return eval

def rgb_to_coords(rgb_string):
    """ Remove 'rgb' from rgb_string, split num_str ["r", "g", "b"]
    convert each num_str to int and
    divide by 255 so that coordinates are between 0 - 1 (YIQ space)
    """
    return [ (int(num_str)/255) for num_str in rgb_string[4:-1].split(',') ]
