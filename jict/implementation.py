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

class jict(defaultdict):
    def __new__(self, nd = None ):
        if isinstance( nd, dict ):
            dt = to_jict(nd)
            return dt

        if 'pymongo' in sys.modules:
            if isinstance(nd, Cursor):
                self.generator = nd
                return next( self.generator )

        return super(jict, self).__new__(self, nd)

    def __init__(self, nd = None):
        self.factory = jict
        defaultdict.__init__( self, self.factory )

    def dict(self, input_dict=None ):
        plain_dict = dict()
        if input_dict is None:
            input_dict = self
        for key in input_dict.keys():
            value = input_dict[key]
            if isinstance(value, jict):
                # print "recurse", value
                plain_dict[key] = self.dict(value)
            else:
                plain_dict[key] = value
        return plain_dict

    def __str__(self):
        return json.dumps( self.dict() , indent = 2 , cls= JSONEncoder )

    def json(self,indent=2):
        return json.dumps( self.dict() , indent = indent , cls= JSONEncoder )
