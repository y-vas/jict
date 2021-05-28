from jict import jict, jictmt
#
jct = jict('shm//:config.yaml')

jct['151'] = 'dsfasd'
jct['153'] = 'aaaaaa'
jct['asdfasd'] = 'afsdf'

jictmt( jct ).main()
