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

class Mock(Transform):
    def visit_amp(self, amp):
        amp.allocate()
        amp.buffer[:] = 1.0 * amp.ref.data / numpy.median(amp.ref.data)
        amp.invvar[:] = (amp.ref.data * 1.0) ** -0.5

