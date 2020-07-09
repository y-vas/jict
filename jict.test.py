from jict import jict

jct = jict('shm://mymemory')
jct['memoryfield'] = ['hi']


jct2 = jict('shm://mymemory')
print( jct2['memoryfield'] )
# output : hi


# python3 setup.py sdist bdist_wheel
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
