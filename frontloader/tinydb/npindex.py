import numpy

class Index(object):
    """ Frozen fast indices of tinydb tables, via numpy 

        Only indexing on one key is supported.
    """

    def __init__(self, table, key, **kwargs):
        self.table = table
        self.key = key
        self.reverse = bool(kwargs.get('reverse'))

        self.key_values = numpy.array([d[key] for d in self.table.all()])
        eids = numpy.array([d.eid for d in self.table.all()]) 
        arg = numpy.argsort(self.key_values)
        self.eids = eids[arg]
        self.sorted = self.key_values[arg]

    def contains(self, value):
        if len(self.sorted) == 0:
            return value != value
        ind = self.sorted.searchsorted(value)
        ind = numpy.clip(ind, 0, len(self.sorted) - 1)
        return self.sorted[ind] == value
    
    def get(self, value):
        ind = self.sorted.searchsorted(value)
        return [self.table.get(eid) for eid in self.eids[ind]]

    def get_eids(self, value):
        ind = self.sorted.searchsorted(value)
        return self.eids[ind]
        
