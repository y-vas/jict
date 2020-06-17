#####################
jict
#####################

.. automodule:: jict

**************************
Class documentation
**************************
.. class:: jict

.. _jict.init:

    .. method:: jict.__init__([existing_dict | nested_level, value_type])

        :param existing_dict: an existing ``dict`` to be converted into a ``jict``
        :param nested_level: the level of nestedness in the dictionary
        :param value_type: the type of the values held in the dictionary

        For example,

            .. <<Python

            .. code-block:: Python

                a = jict(3, list)
                a['level 1']['level 2']['level 3'].append(1)

                b = jict(2, int)
                b['level 1']['level 2']+=3

            ..
                Python

        If nested_level and value_type are not defined, the degree of nested-ness is not
        fixed. For example,

            .. <<Python

            .. code-block:: Python

                a = jict()
                a['1']['2']['3'] = 3
                a['A']['B'] = 15

            ..
                Python

.. _jict.update:

    .. method:: update(other)

        Updates the dictionary recursively with the key/value pairs from other, overwriting existing keys. Return None.

        If the jict has a fixed level of nestedness and a value_type, then this is ignored for the key/value
        pairs from other but otherwise preserved as far as possible.


.. _iteritems_flat:

    .. method:: iteritems_flat()

        python 2.7 style synonym for ``items_flat()``

.. _items_flat:

    .. method:: items_flat()

        iterate through values with nested keys flattened into a tuple

        For example,

            .. code-block:: Python

                from jict import jict
                a = jict()
                a['1']['2']['3'] = 3
                a['A']['B'] = 15

            print list(a.items_flat())

        Produces:

            ::

                [       (('1', '2', '3'),   3),
                        (('A', 'B'),        15)
                ]

.. _iterkeys_flat:

    .. method:: iterkeys_flat()

        python 2.7 style synonym for ``keys_flat()``

.. _keys_flat:

    .. method:: keys_flat()

        iterate through values with nested keys flattened into a tuple

        For example,

            .. code-block:: Python

                from jict import jict
                a = jict()
                a['1']['2']['3'] = 3
                a['A']['B'] = 15

                print list(a.keys_flat())

        Produces:

            ::

                [('1', '2', '3'), ('A', 'B')]

.. _itervalues_flat:

    .. method:: itervalues_flat()

        python 2.7 style synonym for ``values_flat()``

.. _values_flat:

    .. method:: values_flat()

        iterate through values as a single list, without considering the degree of nesting

        For example,

            .. code-block:: Python

                from jict import jict
                a = jict()
                a['1']['2']['3'] = 3
                a['A']['B'] = 15

                print list(a.values_flat())

        Produces:

            ::

                [3, 15]

.. _to_dict:

    .. method:: to_dict()

        Converts the nested dictionary to a nested series of standard ``dict`` objects

        For example,

            .. code-block:: Python

                from jict import jict
                a = jict()
                a['1']['2']['3'] = 3
                a['A']['B'] = 15

                print a.to_dict()

        Produces:
            ::

                {'1': {'2': {'3': 3}}, 'A': {'B': 15}}

    .. method:: __str__([indent])

        The dictionary formatted as a string

        :param indent: The level of indentation for each nested level

        For example,

            .. code-block:: Python

                from jict import jict
                a = jict()
                a['1']['2']['3'] = 3
                a['A']['B'] = 15

                print a
                print a.__str__(4)

        Produces:
            ::

                {"1": {"2": {"3": 3}}, "A": {"B": 15}}
                {
                    "1": {
                        "2": {
                            "3": 3
                        }
                    },
                    "A": {
                        "B": 15
                    }
                }

**************************
Acknowledgements
**************************

    Inspired in part from ideas in:
    http://stackoverflow.com/questions/635483/what-is-the-best-way-to-implement-nested-dictionaries-in-python
    contributed by nosklo

    Many thanks

**************************
Copyright
**************************
    The code is licensed under the MIT Software License
    http://opensource.org/licenses/MIT

    This essentially only asks that the copyright notices in this code be maintained
    for **source** distributions.


