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
ap.add_argument("--force", help="Replace all entries", action='store_true', default=False)
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
        d['FLAVOR'] = 'object'
        d['AIRMASS'] = header['AIRMASS']
    return d

def main():
    filenames = sorted(list(glob(os.path.join(ns.prefix, '*/*.fits.gz'))))
    repo = Repository(ns.prefix, ns.output)
    for filename in filenames:
        PK = os.path.basename(filename)
        print filename, PK,
        if len(repo.search(repo.where('PK') == PK)) > 0:
            print 'exists'
            if not ns.force:
                continue
        try:
            d = scan(filename)
        except Exception as e:
            print 'failed', e
            repo.remove(repo.where("PK") == d["PK"])
            repo.insert(d)
#            repo.flush()

if __name__ == "__main__":
    main()
