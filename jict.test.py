from jict import jict

jct = jict({
    'val': {
        'list':[
            [{
                'password': 'secret'
            }]
        ]
    }
})

# we also can replace values
jct.replace('password','mypass')
print(jct.get('password'))
# output : mypass
# output :
# hi
