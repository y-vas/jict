
class array( list ):
    def __init__(self, *args, **kwargs):
        for arr in args:
            if isinstance(arr,list):
                self.append( array(*arr) )
            else:
                self.append(arr)


    def __str__( self ):
        return 'array::' + str(list(self))

    @property
    def test(self):
        return 'hi'
