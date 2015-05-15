from ..utils import parse_fits_range
from fitsio import FITS
from ..nodes import CCD, Amp

def parse_hdus(exposure):
    fits = FITS(exposure.filename)
    for i in range(1, len(fits)):
        hdu = fits[i]
        header = hdu.read_header()
        ccdname = header['CCDNAME'].strip().upper()
        if ccdname not in exposure:
            ccdsize = parse_fits_range(header['CCDSIZE'])
            ccdsize = ccdsize[0][1], ccdsize[1][1] 
            ccd = CCD(ccdname, ccdsize)
            exposure[ccdname] = ccd
        else:
            ccd = exposure[ccdname]

        # FITS is fortran, we use C
        data = hdu[:, :].T.copy()
        ccdsec = parse_fits_range(header['CCDSEC'], to_python=True)
        datasec = parse_fits_range(header['DATASEC'], to_python=True)
        biassec = parse_fits_range(header['BIASSEC'], to_python=True)
        ccd.push_amp(ccdsec, datasec, biassec, data)

