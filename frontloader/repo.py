from .tinydb import TinyDB
from .tinydb import where
from .tinydb.storages import JSONPrettyStorage
from .tinydb.middlewares import CachingMiddleware
from .tinydb.npindex import Index
from .nodes import Exposure

import os.path
from fitsio import FITS

class Repository(TinyDB):
    """ An interface to the metadata database created by scanner 
        
        The idea is to support queries for a time range etc. 
    """
    def __init__(self, prefix, filename):
        TinyDB.__init__(self, filename, storage=CachingMiddleware(JSONPrettyStorage))
        self.prefix = prefix
    def create_index(self, key):
        return Index(self, key)

    def open(self, key):
        [m] = self.search(where("PK")==key)
        filename = os.path.join(self.prefix, m['PATH'])
        exposure = Exposure(m, filename)
        return exposure

Repository.where = where    
