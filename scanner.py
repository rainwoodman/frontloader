from argparse import ArgumentParser
from glob import glob
import os.path
import fitsio
import json

ap = ArgumentParser()
ap.add_argument("prefix", help="Location to scan the image files")
ap.add_argument("output", help="Location to store the database")

ns = ap.parse_args()

def scan(filename):
    f = fitsio.FITS(filename)
    header = f[0].read_header()
    objecttype = header['OBJECT'].strip().lower()

    d = dict(
        RAWFILENAME=os.path.basename(filename),
        OBJECTYPE=objecttype,
        UTC_OBS=header['UTC-OBS']
    )

    if objecttype == "zero":
        pass
    elif objecttype == "flat":
        pass
    else:
        d['RA'] = header['RA']
        d['DEC'] = header['DEC']
    print d
    return d
def main():
    filenames = list(glob(os.path.join(ns.prefix, '*/*.fits.gz')))
    db = []
    for filename in filenames:
        db.append(scan(filename))
    if ns.output == '-':
        ff = stdout
    else:
        ff = file(ns.output, 'w')
    with ff:
        json.dump(db, ff)

if __name__ == "__main__":
    main()
