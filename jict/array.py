
class array( list ):
    arr = []

    def __init__(self, *args, **kwargs):
        # super(array, self).__init__()
        # inits

        for arr in args:
            self.arr.append(arr)
            if isinstance(arr,list):
                print('Is list', arr)
                self.arr = array(arr)


    def __str__( self ):
        printable = []
        for x in sel.arr:
            val = x
            if isinstance(x,array):
                val = x.arr
            printable.append(val)
        return 'array::' + str( printable )
