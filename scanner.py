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
ap.add_argument("--update", help="Replace all entries", action='store_true', default=False)
ap.add_argument("prefix", help="Location to scan the image files")
ap.add_argument("output", help="Location to store the database")

ns = ap.parse_args()

def parse_hex(hex):
    sp =  hex.split(':')
    base = float(sp[0]) 
    frac = float(sp[1]) / 60. + float(sp[2]) / 3600.
    sgn = 1 if base >= 0 else -1
    return sgn * (sgn * base + frac)

def scan(filename):
    """ BOK file scanner -- extract meta data from files """
    d = dict(
        PK=os.path.basename(filename),
        PATH=os.path.relpath(filename, ns.prefix),
        )
    try:
        f = fitsio.FITS(filename)
        header = f[0].read_header()
        OBJECT = header['OBJECT'].strip().lower()
        d['FLAVOR'] = OBJECT
        d['DATE_OBS'] = header['DATE-OBS'] + 'T' + header['UTC-OBS']

        if OBJECT == "zero":
            pass
        elif OBJECT == "flat":
            pass
        else:
            d['RA'] = parse_hex(header['RA'])
            d['DEC'] = parse_hex(header['DEC'])
            d['FLAVOR'] = 'object'
            d['AIRMASS'] = header['AIRMASS']
    except Exception as e:
        d['OBJECT'] = 'failure'
        d['EXCEPTION'] = str(e)
    return d

def main():
    filenames = sorted(list(glob(os.path.join(ns.prefix, '*/*.fits.gz'))))
    repo = Repository(ns.prefix, ns.output)
    PKindex = repo.create_index('PK')

    for filename in filenames:
        PK = os.path.basename(filename)
        print filename, PK,
        if PKindex.contains(PK):
            print 'exists'
            if ns.update:
                update = True
            else:
                continue
        else:
            update = False
        d = scan(filename)
        if update:
            repo.update(d, eids=PKindex.get_eids([PK]))
        else:
            repo.insert(d)
        repo._storage.flush()
        print d

if __name__ == "__main__":
    main()
