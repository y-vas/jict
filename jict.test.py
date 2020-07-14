from jict import jict , deque, evaluate
from time import sleep

jct = jict( 'set://mymemory.yaml' )

x = 0
while True:
    x += 1
    jct.deque('key', x , 10 )
    print(x)
    sleep(1)
