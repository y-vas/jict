#!/usr/bin/env python
from __future__ import print_function
from __future__ import division

from collections import defaultdict
import sys, json

def to_jict(dict):
    nd = jdict()
    for k,i in dict.items():
        if isinstance(i,dict):
            nd[k] = to_jict(i)
        else:
            nd[k] = i
    return nd

class jict(defaultdict):

    def __init__(self, nd = None ):
        if isinstance(nd,dict):
            self = to_dict(nd)
            return

        self.factory = jict
        defaultdict.__init__(self, self.factory)

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
        return json.dumps(self.dict(), indent = 2 )
