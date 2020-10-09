
from .helpers import jsonencoder
import json

class array( list ):
    def __init__(self, *args, **kwargs):
        for arr in args:
            if isinstance(arr,list):
                self.append( array(*arr) )
            else:
                self.append(arr)

    def __str__( self ):
        return json.dumps(
            list(self) ,
            indent = 2 ,
            cls= jsonencoder
        )

    @property
    def test(self):
        return 'hi'
