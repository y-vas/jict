
class array():

    def __new__(self, *args, **kwargs ):
        for arr in args:
            if isinstance(arr,list):
                print('Is list', arr)
                nwarray += arr
            else:
                print('No list', arr)
        return nwarray
