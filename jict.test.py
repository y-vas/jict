from jict import jict, evaluate
from time import sleep, time

myobj = jict( 'shm://stock' )

while True:
    tm = time()
    myobj['time'] = tm
    print(tm)
    sleep(1)
