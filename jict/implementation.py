#!/usr/bin/env python
from __future__ import print_function
from __future__ import division

from collections import defaultdict
import sys, json
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
    verbose = False
    def __new__(self, nd = None ,verbose = False):
        if isinstance( nd, dict ):
            dt = to_jict(nd)
            dt.verbose = verbose
            return dt

        if 'pymongo' in sys.modules:
            if isinstance(nd, Cursor):
                try:
                    jt = jict( next(nd) ,verbose )
                    jt.generator = nd
                except:
                    jt = jict()
                return jt

        return super(jict, self).__new__(self, nd, verbose )

    def __init__(self, nd = None, verbose = False ):
        self.factory = jict
        self.verbose = verbose
        defaultdict.__init__( self, self.factory )

    def __iter__(self):
        started = False

        if self.generator != None:
            if hasattr(self.generator, 'count') and self.verbose:
                cnt = self.generator.count()
                c = 0
                if not started:
                    started = True
                    yield jict( self.dict() )

                for x in self.generator:
                    ps = 100 / cnt * c
                    print ( "Loading (" + str(ps) + '%)' + "." * int(ps) )
                    c += 1
                    yield to_jict(x)

            else:
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
        return json.dumps( self.dict() , indent = 2 , cls= JSONEncoder )

    def json(self,indent=2):
        return json.dumps( self.dict() , indent = indent , cls= JSONEncoder )
