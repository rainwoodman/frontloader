#TODO:
# convert RA/DEC 00:00:00(sexagesimal) to 00.00 (decimal)
# EXPTIME DATE-POBS FILTER
# FLAVOR
# SCAN DECAM data

from argparse import ArgumentParser
from glob import glob
import os.path
import fitsio
from frontloader import Repository

ap = ArgumentParser()
ap.add_argument("prefix", help="Location to scan the image files")
ap.add_argument("output", help="Location to store the database")

ns = ap.parse_args()

def scan(filename):
    """ DECAM file scanner -- extract meta data from files """
    f = fitsio.FITS(filename)
    header = f[0].read_header()
    try:
        OBJECT = header['OBJECT'].strip().lower()

        d = dict(
            PK=os.path.basename(filename),
            PATH=os.path.relpath(filename, ns.prefix),
            DATE_OBS=header['DATE-OBS'],
        )
        if OBJECT in ['domeflat-u40']:
            d['FLAVOR'] = 'flat'
        elif OBJECT in ['postnight-bias']:
            d['FLAVOR'] = 'zero'
        else:
            d['RA'] = header['RA']
            d['DEC'] = header['DEC']
            d['FLAVOR'] = 'object'
        return d
    except ValueError as e:
        print e
        print sorted(header.keys())
        raise

def main():
    filenames = sorted(list(glob(os.path.join(ns.prefix, '*/*.fits.fz'))))
    with Repository(ns.prefix, ns.output) as db:

        for filename in filenames:
            d = scan(filename)
            db.remove(Repository.where("PK") == d["PK"])
            db.insert(d)


if __name__ == "__main__":
    main()
