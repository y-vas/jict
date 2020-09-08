from eval import eval_base
from jict import jict
from pymongo import MongoClient


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

mg = MongoClient([ "127.0.0.1:27017" ])
db = mg['fintistics']['test']

jct = jict(db,'hi')
eval_base( jct )
jct.save()
