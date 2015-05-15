import numpy

def parse_fits_range(fits_range, to_python=False):
    """ This will parse a fits_range to ((a,b),(c,d)) """
    x, y = fits_range.strip()[1:-1].split(',')
    x = tuple([int(i) for i in x.split(':')])
    y = tuple([int(i) for i in y.split(':')])
    if to_python:
        stepy = 1 if y[1] > y[0] else -1
        stepx = 1 if x[1] > x[0] else -1
        return (slice(x[0] - 1, x[1] + stepx - 1, stepx),
                slice(y[0] - 1, y[1] + stepy - 1, stepy))
    return x, y

