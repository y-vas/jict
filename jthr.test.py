from jict import jict
from time import sleep

myobj = jict( 'shm://stock' )

while True:
    print(myobj['time'])
    sleep(1)
