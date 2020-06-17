#!/usr/bin/env python
"""`jict` provides dictionaries with multiple levels of nested-ness."""
from __future__ import print_function
from __future__ import division

from collections import defaultdict
import sys, json

class jict(defaultdict):

    def __init__(self, nd = None ):
        self.factory = jict
        defaultdict.__init__(self, self.factory)


    def dict(self, input_dict=None ):
        plain_dict = dict()
        if input_dict is None:
            input_dict = self
        for key in input_dict.keys():
            value = input_dict[key]
            if isinstance(value, _recursive_dict):
                # print "recurse", value
                plain_dict[key] = self.dict(value)
            else:
                plain_dict[key] = value
        return plain_dict

    def __str__(self):
        return json.dumps(self.dict(), indent = 2 )
