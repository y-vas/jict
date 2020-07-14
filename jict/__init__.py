#!/usr/bin/env python
"""`jict` provides dictionaries with multiple levels of nested-ness."""

__version__ = '2.4'
from .jict import jict, sqlconnect, evaluate
from collections import deque
from .menu import jictmt

__all__ = ( 'jict', 'sqlconnect', 'evaluate', 'deque', 'jictmt' )
