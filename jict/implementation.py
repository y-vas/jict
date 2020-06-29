#!/usr/bin/env python
from __future__ import print_function
from __future__ import division

from collections import defaultdict
import sys, json,yaml, os
from bson import ObjectId

if 'pymongo' in sys.modules:
    from pymongo.cursor import Cursor

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
                print(nd[-5:])
                if nd[-5:] in [ '.yaml' , '.json' ]:
                    nam, ext = os.path.splitext( nd )

                    file = open( nd, "a+" )
                    text = file.read()
                    file.close()

                    data = {}
                    if ext == '.yaml':
                        print(text)
                        data = yaml.safe_load( text )
                        print( 'dataloaded', data )
                    elif ext == '.json':
                        data = json.loads(text )

                    dt = to_jict( data )
                    dt.storepath = nd
                    print(dt.storepath , nd)
                else:
                    dt = to_jict( json.loads( nd ) )
            except Exception as e:
                print(e)
                dt = jict()
            return dt

        if 'pymongo' in sys.modules:
            if isinstance(nd, Cursor):
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
        return yaml.dump(yaml.load(self.json() , Loader=yaml.FullLoader ), default_flow_style=False)

    def save(self, name = None, tp = None ):
        print( self.storepath )

        self.storepath = name if name != None else self.storepath \
                    if self.storepath != None else 'jict.json'

        nam, ext = os.path.splitext( self.storepath )
        tp = ext if tp == None else '.' + tp if not tp[0] == '.' else tp
        self.storepath = nam + tp

        f = open(self.storepath, "w+")
        f.write( self.yaml() if tp == '.yaml' else self.json() )
        f.close()
