#!/usr/bin/env python
"""`jict` provides dictionaries with multiple levels of nested-ness."""
__version__ = '2.1'
from .implementation import jict, sqlconnect, evaluate

__all__ = ('jict', 'sqlconnect', 'evaluate')
