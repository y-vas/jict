from jict import jict
from time import sleep, time

# this creates a shared memory file 
myobj = jict( 'shm://stock' )

while True:
    tm = time()
    myobj['time'] = tm
    print(tm)
    sleep(1)
