import os.path
import fitsio
import json
import numpy

def parse_fits_range(fits_range):
    """ This will parse a fits_range to ((a,b),(c,d)) """
    x, y = fits_range.strip()[1:-1].split(',')
    x = tuple([int(i) for i in x.split(':')])
    y = tuple([int(i) for i in y.split(':')])
    return x, y

class CCD(object):
    def __init__(self, ccdname, size):
        self.ccdname = ccdname
        self.buffer = numpy.empty(size, dtype='f8')

class Exposure(object):
    def __init__(self, rawimage, metadata):
        self.rawimage = rawimage
        self.metadata = metadata
        self.ccds = {}

        # all HDUs
        for i in range(1, len(self.rawimage)):
            hdu = self.rawimage[i]
            header = hdu.read_header()
            ccdname = header['CCDNAME'].strip().upper()
            if ccdname not in self.ccds:
                ccdsize = parse_fits_range(header['CCDSIZE'])
                ccdsize = ccdsize[0][1], ccdsize[1][1] 
                self.ccds[ccdname] = CCD(ccdname, ccdsize)
            
    def __repr__(self):
        return " CCDs : %s" % ' '.join([ccdname for ccdname in self.ccds])

class Instrument(object):
    def __init__(self, prefix, metadatafile):
        with file(metadatafile, 'r') as ff:
            metadata = json.load(ff)
        self.metadata = dict(
            [(item['PK'], item) for item in metadata])
        self.prefix = prefix

    def open(self, key):
        m = self.metadata[key]
        filename = m['RELFILENAME']

        fits = fitsio.FITS(
            os.path.join(self.prefix, filename)
            )
        return Exposure(fits, m)

def dustin(instru, filename, ccdname):
    """returns image , invvar, mask

       astrometry, photometric zero point
    """

    pass
