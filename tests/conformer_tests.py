import unittest
from unittest import TestCase
from io import StringIO
from token import NAME, OP, NEWLINE, INDENT, NUMBER
from tokenize import COMMENT
from pprint import pprint

from bones.conformer import suppress_mutations
from bones.tokengenerator import generate_tokens
from bones.token_parser import TokenParser
from bones.containers.bones_token import Token


class ConformerTests(TestCase):
    def test_string_funcdefs_are_pythonified(self):
        expected_0 = [
            Token((NAME,'def',(1, 0),(1, 3),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NAME,'_I_m_a_string_funcdef_Wheee_',(1, 4),(1, 34),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP,'(',(1, 34),(1, 35),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP,')',(1, 35),(1, 36),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP,':',(1, 36),(1, 37),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NEWLINE,'\n',(1, 37),(1, 38),'def "I\'m a string funcdef. Wheee!"():\n')),
        ]

        expected_1 = [
            Token((NAME,'def',(4, 0),(4, 3),'def im_a_regular_function():\n')),
            Token((NAME,'im_a_regular_function',(4, 4),(4, 25),'def im_a_regular_function():\n')),
            Token((OP,'(',(4, 25),(4, 26),'def im_a_regular_function():\n')),
            Token((OP,')',(4, 26),(4, 27),'def im_a_regular_function():\n')),
            Token((OP,':',(4, 27),(4, 28),'def im_a_regular_function():\n')),
            Token((NEWLINE,'\n',(4, 28),(4, 29),'def im_a_regular_function():\n')),
        ]

        data = '''\
def "I'm a string funcdef. Wheee!"():
    pass

def im_a_regular_function():
    pass
'''
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        self.assertEqual(expected_0, actual.funcdefs[0].signature)
        self.assertEqual(expected_1, actual.funcdefs[1].signature)

    def test_funcdefs_with_bdd_blocks_are_prefixed_with_test_(self):
        # note: the prefix is 'test_' not 'test'
        expected_0 = [
            Token((NAME, 'def', (1, 0), (1, 3), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NAME, 'test__I_m_a_string_funcdef_Wheee_', (1,  4), (1,  34), 'def "I\'m a string funcdef. Wheee!"():\n')), 
            Token((OP, '(', (1, 34), (1, 35), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP, ')', (1, 35), (1, 36), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP, ':', (1, 36), (1, 37), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NEWLINE, '\n', (1, 37), (1, 38), 'def "I\'m a string funcdef. Wheee!"():\n')),
        ]
        expected_1 = [
            Token((NAME, 'def', (5, 0), (5, 3), 'def im_a_regular_function():\n')),
            Token((NAME, 'im_a_regular_function', (5, 4), (5, 25), 'def im_a_regular_function():\n')),
            Token((OP, '(', (5, 25), (5, 26), 'def im_a_regular_function():\n')),
            Token((OP, ')', (5, 26), (5, 27), 'def im_a_regular_function():\n')),
            Token((OP, ':', (5, 27), (5, 28), 'def im_a_regular_function():\n')),
            Token((NEWLINE, '\n', (5, 28), (5, 29), 'def im_a_regular_function():\n')),
        ]

        data = '''\
def "I'm a string funcdef. Wheee!"():
    then:
        pass

def im_a_regular_function():
    pass
'''
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        self.assertEqual(expected_0, actual.funcdefs[0].signature)
        self.assertEqual(expected_1, actual.funcdefs[1].signature)

    @unittest.skip('')
    def test_bdd_keywords_are_removed(self):
        expected = Token((COMMENT, '#then', (2, 4), (2, 8), '    then:\n'))
        data = '''\
def blah():
    then:
        call_something()
'''
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        for i in bag_of_bones.funcdefs[0].bdd_blocks['then']:
            pprint(bag_of_bones.funcdefs[0].bdd_blocks['then'][i])

        self.assertEqual(expected, actual.funcdefs[0])

    def test_funcdef_body_is_copied(self):
        LINE_TWO = 2
        LINE_THREE = 3
        expected = {
            LINE_TWO: [
                Token((INDENT,  '    ',  (2, 0),  (2, 4), '    dont_forget_me()\n')),
                Token((NAME, 'dont_forget_me', (2, 4), (2, 18), '    dont_forget_me()\n')),
                Token((OP, '(', (2, 18), (2, 19), '    dont_forget_me()\n')),
                Token((OP, ')', (2, 19), (2, 20), '    dont_forget_me()\n')),
                Token((NEWLINE, '\n', (2, 20), (2, 21), '    dont_forget_me()\n')),
            ],
            LINE_THREE: [
                Token((NAME, 'x', (3, 4), (3, 5), '    x = 9\n')),
                Token((OP, '=', (3, 6), (3, 7), '    x = 9\n')),
                Token((NUMBER, '9', (3, 8), (3, 9), '    x = 9\n')),
                Token((NEWLINE, '\n', (3, 9), (3, 10), '    x = 9\n')),
            ]
        }


        data = '''\
def blah():
    dont_forget_me()
    x = 9

    then:
        call_something()
'''
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        self.assertEqual(expected[LINE_TWO], actual.funcdefs[0].body[LINE_TWO])
        self.assertEqual(expected[LINE_THREE], actual.funcdefs[0].body[LINE_THREE])


def _build_bag_of_bones(data):
    original_tokens = generate_tokens(StringIO(data))
    return TokenParser().parse_tokens(original_tokens)