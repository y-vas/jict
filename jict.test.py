from jict import jict , deque, evaluate
from time import sleep

def test():
    jct = jict('set://mymemory.yaml')
    sub = jict('sub://mymemory.yaml')

    for x in range( 1000 ):
        jct.deque('key', x , 10 )
        print( next(sub) )

evaluate(test)
