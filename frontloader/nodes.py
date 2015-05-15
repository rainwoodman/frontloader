import numpy
from .utils import parse_fits_range


__all__ = ['Amp', 'CCD', 'Exposure']

class Amp(object):
    def __init__(self, ind, ccdsec, datasec, biassec, data):
        self.ccdsec = ccdsec
        self.datasec = datasec
        self.biassec = biassec
        self.data = data
        self.ind = ind
    def __repr__(self):
        return "Amp(%s)" % repr(self.ccdsec)

class CCD(object):
    def __init__(self, ccdname, size):
        self.ccdname = ccdname
        self.size = size
        self.buffer = numpy.empty(size, dtype='f4')
        self.invvar = numpy.empty(size, dtype='f4')
        self.mask = numpy.empty(size, dtype='?')
        self.flag = numpy.empty(size, dtype='i2')

        self.amps = []

    def push_amp(self, ccdsec, datasec, biassec, data):
        """ add an amp to the end of amp list 

            For internal use in Exposure only.
        """
        ind = len(self.amps)
        self.amps.append(Amp(ind, ccdsec, datasec, biassec, data))

    def __repr__(self):
        return "%s(%d amps)" % (self.ccdname, len(self.amps))

class Exposure(object):
    def __init__(self, rawimage, metadata):
        self.metadata = metadata
        self.ccds = {}

        for i in range(1, len(rawimage)):
            hdu = rawimage[i]
            header = hdu.read_header()
            ccdname = header['CCDNAME'].strip().upper()
            if ccdname not in self.ccds:
                ccdsize = parse_fits_range(header['CCDSIZE'])
                ccdsize = ccdsize[0][1], ccdsize[1][1] 
                ccd = CCD(ccdname, ccdsize)
                self.ccds[ccdname] = ccd
            else:
                ccd = self.ccds[ccdname]

            # FITS is fortran, we use C
            data = hdu[:, :].T.copy()
            ccdsec = parse_fits_range(header['CCDSEC'], to_python=True)
            datasec = parse_fits_range(header['DATASEC'], to_python=True)
            biassec = parse_fits_range(header['BIASSEC'], to_python=True)
            ccd.push_amp(ccdsec, datasec, biassec, data)

    def __repr__(self):
        return "Exposure(%s)" % ', '.join([repr(ccd) for ccd in self.ccds.values()])

