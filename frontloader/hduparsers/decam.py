from ..utils import parse_fits_range
from fitsio import FITS
from ..nodes import CCD, Amp

def parse_hdus(exposure):
    fits = FITS(exposure.filename)
    for i in range(1, len(fits)):
        hdu = fits[i]
        header = hdu.read_header()
        #print header
        ccdname = "CCD%02d" % int(header['CCDNUM'])
        if ccdname not in exposure:
            ccdsize = parse_fits_range(header['CCDSEC'])
            ccdsize = ccdsize[0][1], ccdsize[1][1] 
            ccd = CCD(ccdname, ccdsize)
            exposure[ccdname] = ccd
        else:
            ccd = exposure[ccdname]

        # FITS is fortran, we use C
        data = hdu[:, :].T.copy()
        ccdseca = parse_fits_range(header['CCDSECA'], to_python=True)
        dataseca = parse_fits_range(header['DATASECA'], to_python=True)
        biasseca = parse_fits_range(header['BIASSECA'], to_python=True)
        ccd.push_amp(ccdseca, dataseca, biasseca, data)
        ccdsecb = parse_fits_range(header['CCDSECB'], to_python=True)
        datasecb = parse_fits_range(header['DATASECB'], to_python=True)
        biassecb = parse_fits_range(header['BIASSECB'], to_python=True)
        ccd.push_amp(ccdsecb, datasecb, biassecb, data)

