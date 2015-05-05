# frontloader
Prototype of the frontloader

C3 Frame Processing Pipeline}

This document describes the calibration files and processing steps to process raw (or minimally processed, such as WISE Level 1) images into calibrated images.  The resulting images would be flux-calibrated, astrometrically calibrated and sky-subtracted with a per-pixel inverse variance image and mask and include a PSF.

Question: Is zodiacal light in the WISE images considered part of the image or  the sky?

The data sets (CAMERA) that we are using:
decam - Dark Energy Camera on the Blanco
	/global/project/projectdirs/cosmo/staging/decam-public
bok - 90Prime camera on the Bok
    /global/project/projectdirs/cosmo/staging/bok
wise - WISE Level 1 images
    /global/project/projectdirs/cosmo/data/wise/merge/merge\_p1bm\_frm
mosaic3 - MOSAIC3 imager to be built for the Mayall in 2015
sdss - Raw SDSS images
unWISE image stacks ?
sdss DR10 images ?


CAMERA/files.json - List of all files and trusted version of header, one set of entries per file
CAMERA/process.json - Description of the processing steps
CAMERA/ccdconfig/DATE.json - Regions of CCD, gain, read nosie, saturation per amp
CAMERA/mask/DATE.fits.gz
CAMERA/xtalk/DATE.json
CAMERA/linearity/DATE.fits.gz - Linearity data (for each amp)
CAMERA/bias/DATE.fits.gz
CAMERA/flat/DATE.fits.gz
CAMERA/fringe/DATE.fits.gz
CAMERA/astrom
CAMERA/psf
CAMERA/photom - Photometric zero points and photometric scatter within the image
CAMERA/sky - Sky level and coefficients for fringe images
CAMERA/crmask - CR masks, or does this live with the reduced data?

The DATE is a string with no whitespace describing the timestamp, and may or may not include clock time.  For example, 2014-08-11 with the date only, or 2014-08-11T02:46:24.683334 with the date and time.  The calibration files should be chosen that precede the timestamp (as defined by DATE-OBS) for each data image.


\textbf{files.json}
	FILENAME - Include the relative path (include the compression suffix also??? Yu: one less `stat' if fz is included.)
       Example for DECam is '2013-02-11/DECam\_00177050.fits.fz'
       Example for Bok is '20150107/d7030.0011.fits.gz'
       Example for WISE Level 1 is '0a/00720a/001/00720a001-w1-int-1b.fits'
    OBSTYPE - 'object', 'dome', 'zero', 'twi'
       Allow arbitrary values for this, where other values would be treated as non-science
       For the DECam files, these map from OBSTYPE='object', 'dome flat', 'zero', ???, ???
       For the Bok files, these map from IMAGETYP= 'object', 'flat', 'zero', ???, ???
    FILTER
       For the DECam files, these map from the first word/s of FILTER, which can be u, g, r, i, z, Y, Empty, solid plate
       For the Bok files, these map from FILTER
       For the WISE Level 1 files, these map from BAND where 1=W1, 2=W2, 3=W3, 4=W4
    DATE-OBS (including time in UTC format)
        For the DECam files, these map from DATE-OBS
        For the Bok files, these map from the concatenation of DATE-OBS + 'T' + UTC
        For the WISE Level 1 files, these map from DATIME
    EXPTIME
         For DECam, Bok, WISE Level 1 files these map directly from EXPTIME
    RA,DEC (of telescope boresight)
    
A version with close to this information exists for the WISE Level 1 frames here:
   /global/project/projectdirs/cosmo/data/wise/merge/merge\_p1bm\_frm/WISE-index-L1b.fits
    
    
The data files have FITS extensions for either each CCD (DECam) or for each amplifier (Bok).  EXTNUM is the name for each of these.

YU: shall we include a flag for this? per CCD or per AMP?
