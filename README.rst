Bones Testing
=============

Write your python tests like this:

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


This is an exploratory framework which extends Python to make writing testing more delicious.

How to play with this while it's under development:
::

    pyton setup.py develop
    bones some_example_tests.py

This framework is based on Groovy's Spock_.

.. _Spock: https://code.google.com/p/spock
