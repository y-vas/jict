#!/usr/bin/env python
"""`jict` provides dictionaries with multiple levels of nested-ness."""

__version__ = '2.2.2'
from .implementation import jict, sqlconnect, evaluate
from collections import deque

__all__ = ('jict', 'sqlconnect', 'evaluate', 'deque')
