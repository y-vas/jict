from jict import jict , deque, evaluate
from time import sleep

jct = jict( 'shm//:config.json' )

x = jct['key']
def stroe():
    global x
    x += 1
    jct.deque('as',x,10)

evaluate(stroe, 50 ,True )


print('ha')
