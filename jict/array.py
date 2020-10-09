
class array( list ):

    def __init__(self, *args, **kwargs):

        for arr in args:
            self.append(arr)
            if isinstance(arr,list):
                print('Is list', arr)
                self.append(array(*arr))
            else:
                self.append(arr)


    def __str__( self ):
        printable = []
        for x in self:
            val = x
            if isinstance(x,array):
                val = list(self)
            printable.append(val)
        return 'array::' + str( printable )
