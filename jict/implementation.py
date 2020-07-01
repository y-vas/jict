#!/usr/bin/env python
from __future__ import print_function
from __future__ import division

from collections import defaultdict
import sys, json,yaml, os, random
from bson import ObjectId
from multiprocessing import Pool
from SharedArray import create, attach, delete

if 'pymongo' in sys.modules:
    from pymongo.cursor import Cursor

# if 'tensorflow' in sys.modules:
#     import tensorflow

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def to_jict(prev):
    nd = jict()
    for k,i in prev.items():
        if isinstance(i,dict):
            nd[k] = to_jict(i)
        elif isinstance(i,list):
            nl = []
            for l in i:
                if isinstance(l,dict):
                    nl.append(to_jict(l))
                else:
                    nl.append(l)
            nd[k] = nl
        else:
            nd[k] = i
    return nd

class jict( defaultdict ):
    generator = None
    storepath = None

    def __new__(self, nd = None ):
        if isinstance( nd, dict ):
            dt = to_jict(nd)
            return dt

        if isinstance( nd, str ):
            try:
                if nd[-5:] in [ '.yaml' , '.json' ]:
                    if not os.path.exists( nd ):
                        open( nd , 'w+' ).close()

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

                    dt = to_jict( data )
                    dt.storepath = nd
                else:
                    dt = to_jict( json.loads( nd ) )
            except Exception as e:
                print(e)
                dt = jict()
            return dt

        if 'pymongo' in sys.modules:
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

    def rreplace(self, targets):
        for k in targets.keys():
            self._change(k,targets[k])

    def _change(self, target , value ):
        for x in self.keys():
            val = self[x]
            if isinstance(val , jict):
                val._change(target, value )
            if x == target:
                self[x] = value

    def drop(self ,target = None):
        for x in list(self.dict()):
            val = self[x]
            if isinstance(val , jict):
                val.drop( target )
            if val == target:
                del self[x]

    def _ittrlist(self,lst,k):
        found = []
        for x in lst:
            if isinstance(x,list):
                found += self._ittrlist(x,k)
                continue
            elif isinstance(x,dict) or isinstance(x,jict):
                found += self._ittrdict(x,k)
        return found

    def _ittrdict(self,dic,k):
        found = []
        for x in dic.keys():
            val = dic[x]

            if x == k:
                found.append(val)
                continue

            if isinstance(val, list):
                found += self._ittrlist(val,k)
                continue

            elif isinstance(val,dict) or isinstance(val,jict):
                found += self._ittrdict(val,k)

        return found

    def get(self,key):

        ret = self._ittrdict(self,key)

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

    def __str__(self):
        return self.json()

    def json(self,indent=2):
        return json.dumps( self.dict() , indent = indent , cls= JSONEncoder )

    def yaml(self):
        return yaml.dump(yaml.full_load( self.json() ), default_flow_style=False)

    def shm(self):
        pass

    def save(self, name = None, tp = None , shm = '' ):
        self.storepath = name if name != None else self.storepath \
                    if self.storepath != None else 'jict.json'

        nam, ext = os.path.splitext( self.storepath )
        tp = ext if tp == None else '.' + tp if not tp[0] == '.' else tp
        self.storepath = nam + tp

        f = open(self.storepath, "w+")
        f.write( self.yaml() if tp == '.yaml' else self.json() )
        f.close()
