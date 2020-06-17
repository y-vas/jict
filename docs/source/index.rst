.. note ::

    * Source code at https://github.com/bunbun/nested-dict
    * Documentation at http://nested-dict.readthedocs.org

##############################################################################
``jict``
##############################################################################

    ``jict`` is a drop-in replacement extending python `dict  <https://docs.python.org/2/library/stdtypes.html#typesmapping>`__ and
    `defaultdict  <https://docs.python.org/2/library/collections.html#collections.defaultdict>`__
    with multiple levels of nesting.

    You can created a deeply nested data structure without laboriously creating all the sub-levels along the way:

      .. <<Python

      .. code-block:: Pycon

        >>> nd= jict()
        >>> # magic
        >>> nd["one"][2]["three"] = 4

      ..
          Python


    Each nested level is created magically when accessed, a process known as "auto-vivification" in perl.


******************************************************************************
Specifying the contained type
******************************************************************************

    You can specify that a particular level of nesting holds a specified **value type**, for example:
        * a collection (like a `set  <https://docs.python.org/2/library/sets.html>`__ or `list <https://docs.python.org/2/tutorial/datastructures.html#more-on-lists>`__) or
        * a scalar with useful default values such as ``int`` or ``str``.


**Examples**:

==============================
*dict* of ``list``\ s
==============================
    .. <<Python

    .. code-block:: Python

            #   nested dict of lists
            nd = jict(2, list)
            nd["mouse"]["2"].append(12)
            nd["human"]["1"].append(12)


    ..
        Python

==============================
*dict* of ``set``\ s
==============================
    .. <<Python

    .. code-block:: Python

            #   nested dict of sets
            nd = jict(2, set)
            nd["mouse"]["2"].add("a")
            nd["human"]["1"].add("b")


    ..
        Python

==============================
*dict* of ``int``\ s
==============================

    .. <<Python

    .. code-block:: Python

            #   nested dict of ints
            nd = jict(2, int)
            nd["mouse"]["2"] += 4
            nd["human"]["1"] += 5
            nd["human"]["1"] += 6

            nd.to_dict()
            #{'human': {'1': 11}, 'mouse': {'2': 4}}


    ..
        Python

==============================
*dict* of ``str``\ s
==============================

    .. <<Python

    .. code-block:: Python

            #   nested dict of strings
            nd = jict(2, str)
            nd["mouse"]["2"] += "a" * 4
            nd["human"]["1"] += "b" * 5
            nd["human"]["1"] += "c" * 6

            nd.to_dict()
            #{'human': {'1': 'bbbbbcccccc'}, 'mouse': {'2': 'aaaa'}}

    ..
        Python

##############################################################################
Iterating through ``jict``
##############################################################################

Iterating through deep or unevenly nested dictionaries is a bit of a pain without recursion.
``nested dict`` allows you to **flatten** the nested levels into `tuple  <https://docs.python.org/2/library/functions.html#tuple>`__\ s before iteration.

You do not need to know beforehand how many levels of nesting you have:

    .. <<Python

    .. code-block:: Python

        from jict import jict
        nd= jict()
        nd["one"] = "1"
        nd[1]["two"] = "1 / 2"
        nd["uno"][2]["three"] = "1 / 2 / 3"

        for keys_as_tuple, value in nd.items_flat():
            print ("%-20s == %r" % (keys_as_tuple, value))

        #   (1, 'two')           == '1 / 2'
        #   ('one',)             == '1'
        #   ('uno', 2, 'three')  == '1 / 2 / 3'

    ..
        Python



jict provides
    * :ref:`items_flat() <items_flat>`
    * :ref:`keys_flat() <keys_flat>`
    * :ref:`values_flat() <values_flat>`

(:ref:`iteritems_flat() <iteritems_flat>`, :ref:`iterkeys_flat() <iterkeys_flat>`, and :ref:`itervalues_flat() <itervalues_flat>` are python 2.7-style synonyms. )

##############################################################################
Converting to / from ``dict``
##############################################################################

The magic of  ``jict`` sometimes gets in the way (of `pickle  <https://docs.python.org/2/library/pickle.html>`__\ ing for example).

We can convert to and from a vanilla python ``dict`` using
    * :ref:`jict.to_dict() <to_dict>`
    * :ref:`the jict constructor <jict.init>`

    .. <<Python

    .. code-block:: Pycon

        >>> from jict import jict
        >>> nd= jict()
        >>> nd["one"] = 1
        >>> nd[1]["two"] = "1 / 2"

        #
        #   convert jict -> dict and pickle
        #
        >>> nd.to_dict()
        {1: {'two': '1 / 2'}, 'one': 1}
        >>> import pickle
        >>> binary_representation = pickle.dumps(nd.to_dict())

        #
        #   convert dict -> jict
        #
        >>> normal_dict = pickle.loads(binary_representation)
        >>> new_nd = jict(normal_dict)
        >>> nd == new_nd
        True

    ..
        Python

##############################################################################
Updating with another dictionary
##############################################################################

    You can use the ``jict.update(other)`` method to merge in the contents of another dictionary.

    If the ``jict`` has a fixed nesting and a **value type**, then key / value pairs will be overridden 
    from the other dict like in Python's standard library ``dict``. Otherwise they will be preserved as far as possible.

    For example, given a three-level nested ``jict`` of ``int``:

            .. <<Python

            .. code-block:: Python

                >>> d1 = jict.jict(3, int)
                >>> d1[1][2][3] = 4
                >>> d1[1][2][4] = 5

                >>> # integers have a default value of zero
                >>> default_value = d1[1][2][5]
                >>> print (default_value)
                0
                >>> print (d1.to_dict())
                {1: {2: {3: 4, 4: 5, 5:0}}}

            ..
                Python


        We can update this with any dictionary, not necessarily a three level ``jict`` of ``int``.

            .. <<Python

            .. code-block:: pycon

                >>> # some other jict
                >>> d2 = jict.jict()
                >>> d2[2][3][4][5] = 6
                >>> d1.update(d2)
                >>> print (d1.to_dict())
                {1: {2: {3: 4, 4: 5, 5: 0}}, 2: {3: {4: {5: 6}}}}

            ..
                Python


        However, the rest of the dictionary maintains has the same default **value type** at the specified level of nesting

            .. <<Python

            .. code-block:: Python

                >>> print (d1[2][3][4][5])
                6
                >>> # d1[2][3][???] == int() even though d1[2][3][4][5] = 6
                >>> print (d1[2][3][5])
                0
            ..
                Python

##############################################################################
``defaultdict``
##############################################################################
``jict`` extends `collections.defaultdict  <https://docs.python.org/2/library/collections.html#collections.defaultdict>`__

You can get arbitrarily-nested "auto-vivifying" dictionaries using `defaultdict  <https://docs.python.org/2/library/collections.html#collections.defaultdict>`__.

    .. <<Python

    .. code-block:: Python

        from collections import defaultdict
        jict = lambda: defaultdict(jict)
        nd = jict()
        nd[1][2]["three"][4] = 5
        nd["one"]["two"]["three"][4] = 5

    ..
        Python

However, only ``jict`` supports a ``dict`` of ``dict`` of ``sets`` etc.


.. toctree::
   :titlesonly:
   :name: class documentation

   jict.rst
