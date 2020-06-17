#!/usr/bin/env python
"""`jict` provides dictionaries with multiple levels of nested-ness."""
from __future__ import print_function
from __future__ import division

from collections import defaultdict
import sys, json


# def flatten_nested_items(dictionary):
#     """
#     Flatten a jict.
#
#     iterate through nested dictionary (with iterkeys() method)
#          and return with nested keys flattened into a tuple
#     """
#     if sys.hexversion < 0x03000000:
#         keys = dictionary.iterkeys
#         keystr = "iterkeys"
#     else:
#         keys = dictionary.keys
#         keystr = "keys"
#     for key in keys():
#         value = dictionary[key]
#         if hasattr(value, keystr):
#             for keykey, value in flatten_nested_items(value):
#                 yield (key,) + keykey, value
#         else:
#             yield (key,), value


class _recursive_dict(defaultdict):



    # def iteritems_flat(self):
    #     """Iterate through items with nested keys flattened into a tuple."""
    #     for key, value in flatten_nested_items(self):
    #         yield key, value


    #
    # def __repr__( self ):
    #     return str(self._dtd(self))
    #
    # def _dtd(self, d):
    #     for k, v in d.items():
    #         if isinstance(v, dict):
    #             d[k] = self._dtd(v)
    #     return dict(d)
    #
    # def dict(self):
    #     return self._dtd(self)


    # def iterkeys_flat(self):
    #     """Iterate through keys with nested keys flattened into a tuple."""
    #     for key, value in flatten_nested_items(self):
    #         yield key
    #
    # def itervalues_flat(self):
    #     """Iterate through values with nested keys flattened into a tuple."""
    #     for key, value in flatten_nested_items(self):
    #         yield value

    items_flat = iteritems_flat
    keys_flat = iterkeys_flat
    values_flat = itervalues_flat

    def dict(self, input_dict=None):
        plain_dict = dict()
        if input_dict is None:
            input_dict = self
        for key in input_dict.keys():
            value = input_dict[key]
            if isinstance(value, _recursive_dict):
                # print "recurse", value
                plain_dict[key] = self.dict(value)
            else:
                # print "plain", value
                plain_dict[key] = value
        return plain_dict

    def __str__(self):
        return json.dumps(self.dict(), indent = 2 )

def _nested_levels( level, nested_type ):
    """Helper function to create a specified degree of nested dictionaries."""
    if level > 2:
        return lambda: _recursive_dict(_nested_levels(level - 1, nested_type))
    if level == 2:
        if isinstance(nested_type, _any_type):
            return lambda: _recursive_dict()
        else:
            return lambda: _recursive_dict(_nested_levels(level - 1, nested_type))
    return nested_type

if sys.hexversion < 0x03000000:
    iteritems = dict.iteritems
else:
    iteritems = dict.items

def jict_from_dict(orig_dict, nd):
    for key, value in iteritems(orig_dict):
        if isinstance(value, (dict,)):
            nd[key] = jict_from_dict(value, jict())
        else:
            nd[key] = value
    return nd

# def _recursive_update(nd, other):
#     for key, value in iteritems(other):
#         if isinstance(value, (dict,)):
#             if isinstance(nd[key], (_recursive_dict,)):
#                 _recursive_update(nd[key], other[key])
#             elif isinstance(nd[key], (dict,)):
#                 nd[key].update(other[key])
#             else:
#                 nd[key] = value
#         else:
#             nd[key] = value
#     return nd

class jict(_recursive_dict):

    # def update(self, other):
    #     """Update recursively."""
    #     _recursive_update(self, other)

    def __init__(self, *param, **named_param ):
        """
        Constructor.

        Takes one or two parameters
            1) int, [TYPE]
            1) dict
        """
        if not len(param):
            self.factory = jict
            defaultdict.__init__(self, self.factory)
            return

        if len(param) == 1:
            # int = level
            if isinstance(param[0], int):
                self.factory = _nested_levels(param[0], _any_type())
                defaultdict.__init__(self, self.factory)
                return
            # existing dict
            if isinstance(param[0], dict):
                self.factory = jict
                defaultdict.__init__(self, self.factory)
                jict_from_dict(param[0], self)
                return

        if len(param) == 2:
            if isinstance(param[0], int):
                self.factory = _nested_levels(*param)
                defaultdict.__init__(self, self.factory)
                return

        raise Exception("jict should be initialised with either "
                        "1) the number of nested levels and an optional type, or "
                        "2) an existing dict to be converted into a nested dict "
                        "(factory = %s. len(param) = %d, param = %s"
                        % (self.factory, len(param), param))
