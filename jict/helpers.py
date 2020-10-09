from time import time
from threading import Thread
import os, json, yaml
from bson.objectid import ObjectId
from collections import deque

def evaluate(foo, itter=1 , threaded = False ):

    if threaded == True:
        def threadedfoo():
            Thread(target = lambda: evaluate(foo,itter) ).start()

        threadedfoo()
        return

    t0 = time()
    for _ in range(itter):
        foo()

    print( time() - t0, "seconds wall time" )

def sqlconnect(str):
    if 'mysql-connector' in nolibs:
        raise Exception('strore sql rquieres \'mysql-connector\' module')

    user,pawd,host,database = re.findall(
        "(.*):(.*)@([0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}):(.*)"
    , str )[0]
    cnt = mysql.connector.connect(
        host = host,
        database = database,
        user = user,
        password = pawd
    )
    return cnt


class jsonencoder( json.JSONEncoder ):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, deque):
            return list(o)
        try:
            return json.JSONEncoder.default(self, o)
        except:
            return str(o)

def loader(nd, ext):
    text = open( nd, "r+" ).read()
    data = {}
    if text.strip() == '':
        return data
    if ext == '.yaml':
        data = yaml.safe_load( text )
    elif ext == '.json':
        data = json.loads( text )
    return data

def file( *args, **kwargs ):
    dirname = os.path.dirname(filestr)
    if os.path.isfile( filestr ):
        return open( *args, **kwargs )

    else:
        if not os.path.exists( dirname ):
            os.makedirs( dirname )

        f = open( *args, **kwargs )
        f.write("")
        f.close()

    return open( *args, **kwargs )
