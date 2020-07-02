from jict import jict, evaluate
from time import sleep, time



myobj = jict( 'shm://stock' )
# jct = jict('jict.json')

# print(jct)
myobj['{hi}'] = []


print( myobj['{hi}'] )
print( myobj['{hi}'] )
# evaluate(test,10000)

# myobj2 = jict('shm://stock')
# print('second')
# print(myobj2['hi'])

# print( jict({
#     'id': jct.get('__id__'),
#     'instrument': jct.get('instrument'),
#     'realized': jct.get('realizedPL'),
#     'units': jct.get('units'),
# }) )
