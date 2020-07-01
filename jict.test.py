from jict import jict
from time import sleep, time
from SharedArray import *

a = create("shm://test", 2 )
print(a)

# a[0] = time()
print( a[0] )
# delete('test')
exit()

myobj = 'hi'

while True:
    a[0] = int(time())
    sleep(1)

    print( a[0] )

    # print( jict({
    #     'id': jct.get('__id__'),
    #     'instrument': jct.get('instrument'),
    #     'realized': jct.get('realizedPL'),
    #     'units': jct.get('units'),
    # }) )
