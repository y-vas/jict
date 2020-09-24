# from multiprocessing import shared_memory
#
# b = shared_memory.ShareableList(range(5))
# print(b.shm.name, b)
# c = shared_memory.ShareableList(name=b.shm.name)
# print(c.shm.name, c)


def goodbye(name, adjective):
    print('Goodbye, %s, it was %s to meet you.' % (name, adjective))
from time import sleep
import atexit
atexit.register(goodbye, 'Donny', 'nice')

sleep(5)
# or:
atexit.register(goodbye, adjective='nice', name='Donny')
