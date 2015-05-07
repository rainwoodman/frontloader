import os.path
import fitsio
import json
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

class Reduced(object):
    """ A deep 'copy' of the exposure. 

        binds reduced data to each Amp and CCD
    """
    def __init__(self, ref):
        self.ref = ref
        if isinstance(ref, Exposure):
            self.ccds = {}
            for ccd in ref.ccds:
                self.ccds[ccd] = Reduced(ref.ccds[ccd])
        else:
            if isinstance(ref, Amp):
                shape = ref.data.shape
            elif isinstance(ref, CCD):
                shape = ref.size
                self.amps = [Reduced(amp) for amp in ref.amps]
            else:
                raise TypeError
            self.buffer = numpy.empty(shape, 'f4')
            self.invvar = numpy.empty(shape, 'f4')


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

class Pipeline(object):
    def __init__(self, instrument,
        operations):
        self.instrument = instrument
        self.operations = operations

    def reduce(self, key):
        exposure = self.instrument.open(key)
        r = Reduced(exposure)
        for op in self.operations:
            op.visit_exposure(r)
        return r

class Operation(object):
    def __init__(self):
        pass

    def visit_exposure(self, expo):
        assert isinstance(expo.ref, Exposure)
        for ccd in expo.ccds:
            self.visit_ccd(expo.ccds[ccd])
            
    def visit_ccd(self, ccd):
        assert isinstance(ccd.ref, CCD)
        for amp in ccd.amps:
            self.visit_amp(amp)

    def visit_amp(self, amp):
        assert isinstance(amp.ref, Amp)
        pass

class Stitch(Operation):
    def visit_ccd(self, ccd):
        self.ccd = ccd
        super(Stitch, self).visit_ccd(ccd)

    def visit_amp(self, amp):
        ccd = self.ccd
        ccd.buffer[amp.ref.ccdsec] = amp.buffer[amp.ref.datasec]
        ccd.invvar[amp.ref.ccdsec] = amp.invvar[amp.ref.datasec]

class Copy(Operation):
    def visit_amp(self, amp):
        amp.buffer[:] = amp.ref.data 
        amp.invvar[:] = (amp.ref.data * 1.0) ** -0.5

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

