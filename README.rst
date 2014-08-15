**Only tested with Python 3.4**

How to play with this while it's under development:
::

    pyton setup.py develop
    bones some_example_tests.py

Bones Testing
=============

A behavior-driven testing framework for Python.

The framework extends the Python to make writing testing simpler.

Here's a basic example of how tests will be written (when the framework is done).

::

    def 'when {a} plus {b} then {c}'():
        given:
            some_setup()

        when:
            a | b | c
            1 | 1 | 2
            2 | 2 | 4
            3 | 3 | 100

        then:
            a + b == c

This framework is based on Groovy's Spock_.

.. _Spock: https://code.google.com/p/spock
