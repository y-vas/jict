from jict import jict, jictmt
#
jct = jict('get://mymemory.yaml')

jct['asdfasd'] = '1'
jct['151'] = 'dsfasd'
jct['153'] = 'aaaaaa'
jct['asdfasd'] = 'afsdf'

jictmt( jct ).main()
