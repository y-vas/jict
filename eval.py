from eval import eval_base
from jict import jict


# check base
jct = jict()
eval_base( jct )

# store env
jct = jict('eval/.env.example')
eval_base( jct )
jct.save('eval/.env')

# store json
jct = jict('eval/test.json')
eval_base( jct )
jct.save()
