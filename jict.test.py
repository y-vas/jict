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


def foo(val):
    val[0][0]['name'] = 'jict'
    return val

# we also can replace with callbacks and multiple values
jct.replace({
    'password':'mypass',
    'list': foo,
})

# callbacks also work with this: jct.replace('list' , foo)

print(jct.get('list'))
# output : mypass
# output :
# hi
