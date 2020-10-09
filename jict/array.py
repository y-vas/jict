
class array():
    arr = []

    def __init__(self, *args, **kwargs):
        # super(array, self).__init__()
        # inits

        for arr in args:
            self.arr.append(arr)
            if isinstance(arr,list):
                print('Is list', arr)
                self.arr.append(array(*arr))
            else:
                self.arr.append(arr)



    def __str__( self ):
        return 'array::' + str(self.arr)
