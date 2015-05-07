from argparse import ArgumentParser
from glob import glob
import os.path
import fitsio
import json
from frontloader import Instrument

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
        RELFILENAME=os.path.relpath(filename, ns.prefix),
        OBJECT=OBJECT,
        UTC_OBS=header['UTC-OBS']
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
    db = []
    for filename in filenames:
        db.append(scan(filename))

    ff = file(ns.output, 'w')
    with ff:
        json.dump(db, ff)
    

if __name__ == "__main__":
    main()
