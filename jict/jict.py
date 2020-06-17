from collections import defaultdict
# import json

class jict( defaultdict ):
    pass
    # def __init__( self ):
    #     nd = lambda: defaultdict( nd )
    #     defaultdict.__init__( self , nd )
    #
    # def __repr__( self ):
    #     return str(self._dtd(self))
    #
    # def _dtd(self, d):
    #     for k, v in d.items():
    #         if isinstance(v, dict):
    #             d[k] = self._dtd(v)
    #     return dict(d)
    #
    # def dict(self):
    #     return self._dtd(self)
