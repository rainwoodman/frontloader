#TODO:
# convert RA/DEC 00:00:00(sexagesimal) to 00.00 (decimal)
# EXPTIME DATE-POBS FILTER
# FLAVOR
# SCAN DECAM data

from argparse import ArgumentParser
from glob import glob
import os.path
import fitsio
from frontloader import Metadata

ap = ArgumentParser()
ap.add_argument("prefix", help="Location to scan the image files")
ap.add_argument("output", help="Location to store the database")

ns = ap.parse_args()

def scan(filename):
    """ BOK file scanner -- extract meta data from files """
    f = fitsio.FITS(filename)
    header = f[0].read_header()
    OBJECT = header['OBJECT'].strip().lower()

    d = dict(
        PK=os.path.basename(filename),
        PATH=os.path.relpath(filename, ns.prefix),
        FLAVOR=OBJECT,
        DATE_OBS=header['DATE-OBS'] + 'T' + header['UTC-OBS'],
    )

    if OBJECT == "zero":
        pass
    elif OBJECT == "flat":
        pass
    else:
        d['RA'] = header['RA']
        d['DEC'] = header['DEC']
        d['OBJECT'] = 'object'
    return d

def main():
    filenames = sorted(list(glob(os.path.join(ns.prefix, '*/*.fits.gz'))))
    with Metadata(ns.output) as db:

        for filename in filenames:
            d = scan(filename)
            db.insert(d)


if __name__ == "__main__":
    main()
