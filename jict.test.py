from jict import jict , deque, evaluate
from time import sleep

def test():
    jct = jict('set://mymemory.yaml')
    jcg = jict('get://mymemory.yaml')

    for x in range( 1000 ):
        jct.deque('key', x , 10 )
        jcg['key']

evaluate(test)
