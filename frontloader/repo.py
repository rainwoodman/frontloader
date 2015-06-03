from .tinydb import TinyDB
from .tinydb import where
from .tinydb.storages import JSONPrettyStorage
from .tinydb.middlewares import CachingMiddleware
from .tinydb.index import Index
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
        self.index_by_date_obs = Index(self, 'DATE-OBS')

    def open(self, key):
        [m] = self.search(where("PK")==key)
        filename = os.path.join(self.prefix, m['PATH'])
        exposure = Exposure(m, filename)
        return exposure

    def __getitem__(self, index):
        """ Do not use this frequently. It is slow as horror. """
        return self.index_by_date_obs[index]['PK']

Repository.where = where    
