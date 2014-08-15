from unittest import TestCase
import unittest
from token import NAME, OP, NEWLINE, INDENT, NUMBER, STRING
from tokenize import COMMENT

from bones.conformer import suppress_mutations
from bones.token_parser import parse_tokens
from bones.containers.bones_token import Token
from tests.utils import generate_toks


class ConformerTests(TestCase):

    def test_string_funcdefs_are_pythonified(self):
        data = '''\
def "I'm a string funcdef. Wheee!"():
    pass

def im_a_regular_function():
    pass
'''
        expected_0 = [
            Token((NAME, 'def', (1, 0), (1, 3), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NAME, '_I_m_a_string_funcdef_Wheee_', (1, 4), (1, 34), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP, '(', (1, 34), (1, 35), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP, ')', (1, 35), (1, 36), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP, ':', (1, 36), (1, 37), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NEWLINE, '\n', (1, 37), (1, 38), 'def "I\'m a string funcdef. Wheee!"():\n'))]

        expected_1 = [
            Token((NAME, 'def', (4, 0), (4, 3), 'def im_a_regular_function():\n')),
            Token((NAME, 'im_a_regular_function', (4, 4), (4, 25), 'def im_a_regular_function():\n')),
            Token((OP, '(', (4, 25), (4, 26), 'def im_a_regular_function():\n')),
            Token((OP, ')', (4, 26), (4, 27), 'def im_a_regular_function():\n')),
            Token((OP, ':', (4, 27), (4, 28), 'def im_a_regular_function():\n')),
            Token((NEWLINE, '\n', (4, 28), (4, 29), 'def im_a_regular_function():\n'))]
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        self.assertEqual(expected_0, actual.funcdefs[0].signature)
        self.assertEqual(expected_1, actual.funcdefs[1].signature)

    def test_funcdefs_with_bdd_blocks_are_prefixed_with_test_(self):
        # note: the prefix is 'test_' not 'test'
        data = '''\
def "I'm a string funcdef. Wheee!"():
    then:
        pass

def im_a_regular_function():
    pass
'''
        expected_0 = [
            Token((NAME, 'def', (1, 0), (1, 3), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((
                NAME, 'test__I_m_a_string_funcdef_Wheee_', (1, 4), (1, 34),
                'def "I\'m a string funcdef. Wheee!"():\n')),
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
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        self.assertEqual(expected_0, actual.funcdefs[0].signature)
        self.assertEqual(expected_1, actual.funcdefs[1].signature)

    def test_bdd_keywords_are_commented_out(self):
        # TODO, not sure if removing the tokens completely will screw up the untokenizer, so i'm leaving them in for now. Explore later.
        expected = [Token((COMMENT, '#then', (2, 4), (2, 8), '    then:\n'))]
        data = '''\
def blah():
    then:
        pass
'''
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        self.assertEqual(expected, actual.funcdefs[0].body[2])

    def test_funcdef_body_is_copied(self):
        data = '''\
def blah():
    dont_forget_me()
    x = 9

    then:
        call_something()
'''
        LINE_TWO = 2
        LINE_THREE = 3
        expected = {
            LINE_TWO: [
                Token((INDENT, '    ', (2, 0), (2, 4), '    dont_forget_me()\n')),
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
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        self.assertEqual(expected[LINE_TWO], actual.funcdefs[0].body[LINE_TWO])
        self.assertEqual(expected[LINE_THREE], actual.funcdefs[0].body[LINE_THREE])

    def test_bdd_blocks_are_dedented_and_converted_to_assert_statements(self):
        # given
        data = '''\
def blah():
    then:
        foo == bar(bat='baz')
        poo == far(fat=wowzer())
'''
        expected_3 = [Token((INDENT, '    ', (3, 0), (3, 4), "    assert foo==bar(bat='baz')\n")),
                      Token((NAME, 'assert ', (3, 4), (3, 11), "    assert foo==bar(bat='baz')\n")),
                      Token((NAME, 'foo', (3, 11), (3, 14), "    assert foo==bar(bat='baz')\n")),
                      Token((OP, '==', (3, 14), (3, 16), "    assert foo==bar(bat='baz')\n")),
                      Token((NAME, 'bar', (3, 16), (3, 19), "    assert foo==bar(bat='baz')\n")),
                      Token((OP, '(', (3, 19), (3, 20), "    assert foo==bar(bat='baz')\n")),
                      Token((NAME, 'bat', (3, 20), (3, 23), "    assert foo==bar(bat='baz')\n")),
                      Token((OP, '=', (3, 23), (3, 24), "    assert foo==bar(bat='baz')\n")),
                      Token((STRING, "'baz'", (3, 24), (3, 29), "    assert foo==bar(bat='baz')\n")),
                      Token((OP, ')', (3, 29), (3, 30), "    assert foo==bar(bat='baz')\n")),
                      Token((NEWLINE, '\n', (3, 30), (3, 31), "    assert foo==bar(bat='baz')\n"))]

        expected_4 = [Token((NAME, 'assert ', (4, 4), (4, 11), '    assert poo==far(fat=wowzer())\n')),
                      Token((NAME, 'poo', (4, 11), (4, 14), '    assert poo==far(fat=wowzer())\n')),
                      Token((OP, '==', (4, 14), (4, 16), '    assert poo==far(fat=wowzer())\n')),
                      Token((NAME, 'far', (4, 16), (4, 19), '    assert poo==far(fat=wowzer())\n')),
                      Token((OP, '(', (4, 19), (4, 20), '    assert poo==far(fat=wowzer())\n')),
                      Token((NAME, 'fat', (4, 20), (4, 23), '    assert poo==far(fat=wowzer())\n')),
                      Token((OP, '=', (4, 23), (4, 24), '    assert poo==far(fat=wowzer())\n')),
                      Token((NAME, 'wowzer', (4, 24), (4, 30), '    assert poo==far(fat=wowzer())\n')),
                      Token((OP, '(', (4, 30), (4, 31), '    assert poo==far(fat=wowzer())\n')),
                      Token((OP, ')', (4, 31), (4, 32), '    assert poo==far(fat=wowzer())\n')),
                      Token((OP, ')', (4, 32), (4, 33), '    assert poo==far(fat=wowzer())\n')),
                      Token((NEWLINE, '\n', (4, 33), (4, 34), '    assert poo==far(fat=wowzer())\n'))]
        bag_of_bones = _build_bag_of_bones(data)

        # when
        actual = suppress_mutations(bag_of_bones)

        # then
        self.assertEqual(expected_3, actual.funcdefs[0].body[3])
        self.assertEqual(expected_4, actual.funcdefs[0].body[4])

def _build_bag_of_bones(data):
    original_tokens = generate_toks(data)
    return parse_tokens(original_tokens)
