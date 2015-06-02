import numpy
from .nodes import Exposure, Amp, CCD
__all__ = ['Pipeline', 'Transform']

class ImgenNode(object):
    def __init__(self, ref):
        self.ref = ref

    def allocate(self):
        self.buffer = numpy.empty(self.shape, 'f4')
        self.invvar = numpy.empty(self.shape, 'f4')

    def deallocate(self):
        del self.buffer
        del self.invvar

class ImgenAmp(ImgenNode):
    def __init__(self, ref):
        assert isinstance(ref, Amp)
        super(ImgenAmp, self).__init__(ref)
    @property
    def shape(self):
        return self.ref.data.shape

class ImgenCCD(ImgenNode):
    def __init__(self, ref):
        assert isinstance(ref, CCD)
        self.amps = {}
        for i, amp in enumerate(ref):
            self.amps[i] = ImgenAmp(amp)

        super(ImgenCCD, self).__init__(ref)
    @property
    def shape(self):
        return self.ref.size

    def __getitem__(self, key):
        return self.amps[key]
    def __iter__(self):
        return iter(self.amps)
    def __contains__(self, key):
        return key in self.amps

class ImgenExposure(ImgenNode):
    """ A deep 'copy' of the exposure. 

        binds reduced data to each Amp and CCD
    """
    def __init__(self, ref):
        assert isinstance(ref, Exposure)
        super(ImgenExposure, self).__init__(ref)
        self.ccds = {}
        for ccd in ref:
            self.ccds[ccd] = ImgenCCD(ref[ccd])

    def __getitem__(self, key):
        return self.ccds[key]
    def __iter__(self):
        return iter(self.ccds)
    def __contains__(self, key):
        return key in self.ccds

class Pipeline(object):
    def __init__(self, transforms):
        self.transforms = transforms

    def reduce(self, node):
        if isinstance(node, Exposure):
            r = ImgenExposure(node)
            for op in self.transforms:
                op.visit_exposure(r)
        if isinstance(node, CCD):
            r = ImgenCCD(node)
            for op in self.transforms:
                op.visit_ccd(r)
        if isinstance(node, Amp):
            r = ImgenAmp(node)
            for op in self.transforms:
                op.visit_amp(r)
        return r

class Transform(object):
    def __init__(self):
        pass

    def visit_exposure(self, expo):
        assert isinstance(expo, ImgenExposure)
        for ccd in expo:
            self.visit_ccd(expo[ccd])
            
    def visit_ccd(self, ccd):
        assert isinstance(ccd, ImgenCCD)
        for amp in ccd:
            self.visit_amp(ccd[amp])

    def visit_amp(self, amp):
        assert isinstance(amp, ImgenAmp)
        pass

