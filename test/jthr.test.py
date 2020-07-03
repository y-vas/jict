from jict import jict
from time import sleep

# this is going to check if there is a shared memory and if so we are going to extract
# the time field from it
myobj = jict( 'shm://stock' )

while True:
    print(myobj['time'])
    sleep(1)
