
class array():
    arr = []

    def __init__(self, *args, **kwargs):
        super(array, self).__init__()
        # inits

        for arr in args:
            if isinstance(arr,list):
                print('Is list', arr)

                
    def __str__( self ):
        return str(self.arr)
