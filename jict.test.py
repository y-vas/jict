from jict import jict

jct = jict('shm://mymemory')
jct['memoryfield'] = ['hi']


jct2 = jict('shm://mymemory')
print( jct2['memoryfield'] )
# output : hi
