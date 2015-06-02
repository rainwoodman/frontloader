from ..imgen import Transform
import numpy

class Stitch(Transform):
    def visit_ccd(self, ccd):
        self.ccd = ccd
        ccd.allocate()
        super(Stitch, self).visit_ccd(ccd)

    def visit_amp(self, amp):
        ccd = self.ccd
        ccd.buffer[amp.ref.ccdsec] = amp.buffer[amp.ref.datasec]
        ccd.invvar[amp.ref.ccdsec] = amp.invvar[amp.ref.datasec]
        amp.deallocate()

class ElectronicBias(Transform):
    """
        Electronic Bias Calibration;
        We reject the max and min in the bias region for each scanline.
        Is this done correctly?
    """
    def __init__(self, overscantrim=5):
        self.overscantrim = overscantrim

    def visit_amp(self, amp):
        ost = self.overscantrim 
        eb = amp.buffer[amp.ref.biassec][ost:-ost, :]
        ebmin = eb.min(axis=0)
        ebmax = eb.max(axis=0) 
        ebsum = eb.sum(axis=0) 
        ebsum -= ebmax 
        ebsum -= ebmin 
        ebsum /= (eb.shape[0] - 2) 
        amp.buffer[amp.ref.datasec] -= ebsum[None, :] 

class Initialize(Transform):
    def visit_amp(self, amp):
        amp.allocate()
        amp.buffer[:] = 1.0 * amp.ref.data
        amp.invvar[:] = (amp.ref.data * 1.0) ** -0.5

