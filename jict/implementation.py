#!/usr/bin/env python
from __future__ import print_function
from __future__ import division

from collections import defaultdict , deque
import sys, json, yaml, os, random, re ,copy
from bson.objectid import ObjectId
from pymongo.cursor import Cursor
from time import time

nolibs = []

try:
    import mysql.connector
except:
    nolibs.append('mysql-connector')

# if 'tensorflow' in sys.modules:
#     import tensorflow

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        if isinstance(o, deque):
            return list(o)

        try:
            return json.JSONEncoder.default(self, o)
        except:
            return str(o)

def sqlconnect(str):
    if 'mysql-connector' in nolibs:
        raise Exception('strore sql rquieres \'mysql-connector\' module')

    user,pawd,host,database = re.findall(
        "(.*):(.*)@([0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}):(.*)"
    , str )[0]

    cnt = mysql.connector.connect(
        host=host, database=database, user=user, password=pawd
    )

    return cnt

def evaluate(foo, itter=1 , threads = 1 ):
    # if threads > 1:
    #     for _ in range(threads):
    #         t = Thread(target=tht)

    t0 = time()
    for _ in range(itter):
        foo()
    print( time() - t0, "seconds wall time" )

def loader(nd):
    nam, ext = os.path.splitext( nd )

    file = open( nd, "r+" )
    text = file.read()
    file.close()

    data = {}
    if ext == '.yaml' and text.strip() != '':
        data = yaml.safe_load( text )
    elif ext == '.json':
        data = json.loads(text )
    elif text.strip() == '':
        data = {}

    return data

def to_jict(prev):
    nd = jict()
    for k,i in prev.items():
        if isinstance(i,dict):
            nd[k] = to_jict(i)

        # elif isinstance(i,list):
        #     nl = []
        #     for l in i:
        #         if isinstance(l,dict):
        #             nl.append(to_jict(l))
        #         else:
        #             nl.append(l)
        #     nd[k] = nl

        else:
            nd[k] = i
    return nd

def subscribe(file):
    jct = jict( file )
    jct.subsc = True
    jct.storepath = file
    while True:
        yield jct

class jict( defaultdict ):
    generator = None
    storepath = None

    def __new__(self, nd = None ):
        if isinstance( nd, dict ):
            dt = to_jict(nd)
            return dt

        if isinstance( nd, str ):
            try:
                if len(nd) >= 5 and nd[-5:] in [ '.yaml' , '.json' ]:
                    share, subsc = False ,False

                    if nd[:6] == 'set://':
                        share = True
                        nd = nd[6:]
                    elif nd[:6] == 'get://':
                        subsc = True
                        nd = nd[6:]
                    elif nd[:6] == 'sub://':
                        return subscribe(nd[6:])

                    if not os.path.exists( nd ):
                        open( nd , 'w+' ).close()

                    dt = to_jict( loader(nd) )
                    if share: dt.share = True
                    if subsc: dt.subsc = True
                    dt.storepath = nd
                else:
                    dt = to_jict( json.loads( nd ) )
            except Exception as e:
                print(e)
                dt = jict()
            return dt

        if isinstance( nd, Cursor ):
            try:
                jt = jict( next(nd) )
                jt.generator = nd
            except:
                jt = jict()
            return jt

        return super(jict, self).__new__(self, nd )

    def __init__(self, nd = None ):
        self.factory = jict
        defaultdict.__init__( self, self.factory )

    def __iter__(self):
        started = False

        if self.generator != None:
            if not started:
                started = True
                yield jict(self.dict())

            for x in self.generator:
                yield to_jict(x)

    def init(self,key,deft):
        if key in self.keys():
            return self[key]
        self[key] = deft
        return self[key]

    def __iadd__(self, other):
        typ = type(other)

        if typ == int:
            return 0 + other

        if typ == dict:
            other = jict(other)
            typ = jict

        if typ == jict:
            for x in other.keys():
                if x not in self.keys():
                    self[x] = other[x]
                else:
                    self[x] += other[x]

        return self

    def increase(self,key,val,create = False ):
        if key not in self.keys():
            if not create: return self[key]
            else:
                self[key] = val
                return self[key]
        self[key] = val if val > self[key] else self[key]
        return self[key]

    def decrease(self,key,val,create = False ):
        if key not in self.keys():
            if not create: return self[key]
            else:
                self[key] = val
                return self[key]
        self[key] = val if val < self[key] else self[key]
        return self[key]

    def drop(self ,target = None):

        def ittrlis(val,tar):
            for l in val:
                if isinstance(l,jict):
                    l.drop(tar)
                if isinstance(l,list):
                    ittrlis(l,tar)

        for x in self.keys():
            val = self[x]
            if isinstance(val , jict):
                val.drop( target )

            if isinstance(val , list ):
                ittrlis(val, target)

            if val == target:
                del self[x]

    def rename(self,target,replace):
        def ittrlist(lst,tg,rp):
            nl = []
            for x in lst:
                if isinstance(x,jict):
                    x.rename(tg,rp)
                if isinstance(x,dict):
                    jct = jict(x)
                    jct.rename(tg,rp)
                    x = jct.dict()
                if isinstance(x,list):
                    x = ittrlist(x,tg,rp)

                nl.append(x)
            return nl

        for k in self.keys():
            val = self[k]
            if isinstance(val,list):
                self[k] = ittrlist(val,target,replace)
            if isinstance(val,jict):
                val.rename(target,replace)
            if isinstance(val,dict):
                jct = jict(val)
                jct.rename(target,replace)
                self[k] = jct.dict()
            if k == target:
                self[replace] = self.pop(target)

    def replace(self, target , replacef = None ):

        if replacef == None and isinstance(target,dict):
            for k in target.keys():
                self.replace(k,target[k])
            return

        def ittrlist(lst,tg,rp):
            nl = []
            for x in lst:
                if isinstance(x,jict):
                    x.replace(tg,rp)
                if isinstance(x,dict):
                    jct = jict(x)
                    jct.replace(tg,rp)
                    x = jct.dict()
                if isinstance(x,list):
                    x = ittrlist(x,tg,rp)
                nl.append(x)
            return nl

        for k in self.keys():
            val = self[k]
            if isinstance(val,list):
                self[k] = ittrlist(val,target,replacef)
            if isinstance(val,jict):
                val.replace(target,replacef)
            if isinstance(val,dict):
                jct = jict(val)
                jct.replace(target,replacef)
                self[k] = jct.dict()

            if k == target:
                if hasattr(replacef, '__call__'):
                    self[k] = replacef(val)
                else:
                    self[k] = replacef

    def _ittrlist(self,lst,k,luky=True ):
        found = []
        for x in lst:
            if isinstance(x,list):
                found += self._ittrlist(x,k,luky)
                continue
            elif isinstance(x,dict) or isinstance(x,jict):
                found += self._ittrdict(x,k,luky)
        return found

    def _ittrdict(self,dic,k ,luky = True ):
        found = []
        for x in dic.keys():
            val = dic[x]

            if x == k:
                found.append(val)
                if luky: return found
                continue

            if isinstance(val, list):
                found += self._ittrlist(val,k,luky)
                continue

            elif isinstance(val,dict) or isinstance(val,jict):
                found += self._ittrdict(val,k,luky)

        return found

    def get(self,key,luky = True ):
        ret = self._ittrdict(self,key, luky )

        if len(ret) == 1:
            return ret[-1]
        elif len(ret) > 1:
            return ret

        return None

    def dict(self, input_dict=None ):
        plain_dict = dict()
        if input_dict is None:
            input_dict = self
        for key in input_dict.keys():
            value = input_dict[key]
            if isinstance(value, jict):
                plain_dict[ key ] = self.dict(value)
            else:
                plain_dict[ key ] = value
        return plain_dict

    def random(self):
        for x in range( random.randint(0, 9) ):
            self[x] = x
            if random.randint(0, 1) == 0:
                self[x] = [ f for f in range(random.randint(0, 10)) ]

    def __str__(self):
        return self.json()

    def json(self,indent=2):
        if indent == 0: return json.dumps( self.dict() , cls= JSONEncoder )
        return json.dumps( self.dict() , indent = indent , cls= JSONEncoder )

    def yaml(self):
        return yaml.dump(yaml.full_load( self.json(0) ), default_flow_style=False)

    def __getitem__(self,key):
        jct = super( defaultdict, self ).__getitem__(key)

        if hasattr( self , 'subsc' ):
            jct = jict( self.storepath  )
            return jct[key]

        return jct

    def __setitem__( self , key , data ):
        super(defaultdict, self).__setitem__( key , data )

        if hasattr( self , 'share' ):
            self.save()

    def deque(self,key,data,maxlen = 5 ):
        if not isinstance(self[key],deque):
            self[key] = deque(maxlen = maxlen)

        self[key].append(data)
        if hasattr(self,'share'):
            self.save()

    def save(self, name = None, tp = None , shm = '' ):

        if name != None:

            valid = ['sql://']

            for x in valid:
                if len(name) >= len(x) and name[:len(x)] == x:
                    if name[:len(x)] == 'sql://':
                        self.sql_store(name[len(x):])
                        return


        self.storepath = name if name != None else self.storepath \
                    if self.storepath != None else 'jict.json'

        nam, ext = os.path.splitext( self.storepath )
        tp = ext if tp == None else '.' + tp if not tp[0] == '.' else tp
        self.storepath = nam + tp

        f = open(self.storepath, "w+")
        f.write( self.yaml() if tp == '.yaml' else self.json() )
        f.close()

    def sql_store(self,db):
        connection = sqlconnect()

        skip = ['columns']

        for table in self.keys():
            lines = self[table]

            if table in skip:
                continue

            for line in lines:
                print( line )

        cursor.close()
        connection.close()

        del cursor
        del connection
