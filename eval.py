from eval import eval_base
from jict import jict


# check base
jct = jict()
eval_base( jct )

# store env
jct = jict('eval/.env.example')
eval_base( jct )
jct.save('eval/.env')

jct = jict('eval/tes.json')
eval_base( jct )
jct.save()
