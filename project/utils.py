def str_px_to_float(string_px):
    """ remove 'px' from string pixel value and return float """
    if string_px[-2:] == 'px':
        return float(string_px[:-2])
    # if type(string_px) == type(int()):
    return float(string_px)

def rgb_to_coords(rgb_string):
    """ Convert rgb string to (decimal) coords """
    numbers_as_s = rgb_string[4:-1]
    numbers_as_l = numbers_as_s.split(',')

    return [(int(i)/255) for i in numbers_as_l]

def rgb_to_1d(rgb_string, sat_thr=0.2, val_thr_b=0.1, val_thr_u=1):
    """ Determine if rgb value is "colourful" or not
    convert rgb to hsv model (better suited for task/less complex):

        hue: ignored (actual colour doesn't matter)
        sat: dull (low) to intense (high) colour
        val: black (low) to white (high) lightness

    So if sat too dull or val too dark or bright, it's 0, else 1
    """

    r, g, b = rgb_to_coords(rgb_string)
    hue, sat, val = colorsys.rgb_to_hsv(r, g, b)
    eval = (sat < sat_thr or val_thr_b > val or val > val_thr_u)

    result = 0 if eval else 1

    return result
