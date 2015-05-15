import numpy


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

class CCD(list):
    def __init__(self, ccdname, size):
        self.ccdname = ccdname
        self.size = size

    def push_amp(self, ccdsec, datasec, biassec, data):
        """ add an amp to the end of amp list 

            For internal use in Exposure only.
        """
        ind = len(self)
        self.append(Amp(ind, ccdsec, datasec, biassec, data))

    def __repr__(self):
        return "%s(%d amps)" % (self.ccdname, len(self))

class Exposure(dict):
    def __init__(self, metadata, filename):
        self.metadata = metadata
        self.filename = filename

    def __repr__(self):
        return "Exposure(%s)" % ', '.join([repr(ccd) for ccd in self.values()])

