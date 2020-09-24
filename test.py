from multiprocessing import shared_memory
import sys
from time import sleep

if 'ss' in sys.argv:
    b = shared_memory.ShareableList(range(5),name='ss')
    while True:
        sleep(1)
        print( b )

c = shared_memory.ShareableList(name='ss')
c[0] = 4
print(c.shm.name, c)
# c.shm.close()
# c.shm.unlink()
# del c  # Use of a ShareableList after call to unlink() is unsupported

#
# def goodbye(name, adjective):
#     print('Goodbye, %s, it was %s to meet you.' % (name, adjective))
# from time import sleep
# import atexit
# atexit.register(goodbye, 'Donny', 'nice')
#
# sleep(5)
# # or:
# atexit.register(goodbye, adjective='nice', name='Donny')
