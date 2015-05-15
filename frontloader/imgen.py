import numpy
from .nodes import Exposure, Amp, CCD
__all__ = ['Pipeline', 'Transform']

class Image(object):
    """ A deep 'copy' of the exposure. 

        binds reduced data to each Amp and CCD
    """
    def __init__(self, ref):
        self.ref = ref
        if isinstance(ref, Exposure):
            self.ccds = {}
            for ccd in ref.ccds:
                self.ccds[ccd] = Image(ref.ccds[ccd])
        else:
            if isinstance(ref, Amp):
                self.shape = ref.data.shape
            elif isinstance(ref, CCD):
                self. shape = ref.size
                self.amps = [Image(amp) for amp in ref.amps]
            else:
                raise TypeError

    def allocate(self):
        self.buffer = numpy.empty(self.shape, 'f4')
        self.invvar = numpy.empty(self.shape, 'f4')

    def deallocate(self):
        del self.buffer
        del self.invvar

class Pipeline(object):
    def __init__(self, transforms):
        self.transforms = transforms

    def reduce(self, exposure):
        r = Image(exposure)
        for op in self.transforms:
            op.visit_exposure(r)
        return r

class Transform(object):
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

