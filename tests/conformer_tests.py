from unittest import TestCase
from token import NAME, OP, NEWLINE, INDENT, NUMBER, STRING
from tokenize import COMMENT

from bones.conformer import suppress_mutations, _extract_operands, _build_assertEquals_tokens
from bones.token_parser import parse_tokens
from bones.containers.bones_token import Token
from tests.utils import generate_toks


class ConformerTests(TestCase):
    def test_string_funcdefs_are_pythonified(self):
        expected_0 = [
            Token((NAME, 'def', (1, 0), (1, 3), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NAME, '_I_m_a_string_funcdef_Wheee_', (1, 4), (1, 34), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP, '(', (1, 34), (1, 35), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP, ')', (1, 35), (1, 36), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP, ':', (1, 36), (1, 37), 'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NEWLINE, '\n', (1, 37), (1, 38), 'def "I\'m a string funcdef. Wheee!"():\n')),
        ]

        expected_1 = [
            Token((NAME, 'def', (4, 0), (4, 3), 'def im_a_regular_function():\n')),
            Token((NAME, 'im_a_regular_function', (4, 4), (4, 25), 'def im_a_regular_function():\n')),
            Token((OP, '(', (4, 25), (4, 26), 'def im_a_regular_function():\n')),
            Token((OP, ')', (4, 26), (4, 27), 'def im_a_regular_function():\n')),
            Token((OP, ':', (4, 27), (4, 28), 'def im_a_regular_function():\n')),
            Token((NEWLINE, '\n', (4, 28), (4, 29), 'def im_a_regular_function():\n')),
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

    def test_bdd_keywords_are_commented_out(self):
        # TODO, not sure if removing the tokens completely will screw up the untokenizer, so i'm leaving them in for now. Explore later.
        expected = Token((COMMENT, '#then', (2, 4), (2, 8), '    then:\n'))
        data = '''\
def blah():
    then:
        pass
'''
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        self.assertEqual(expected, actual.funcdefs[0].body[2])

    def test_funcdef_body_is_copied(self):
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

    def test_bdd_blocks_are_dedented_and_converted_to_assertEquals(self):
        # given
        data = '''\
def blah():
    then:
        foo == bar
        bat == baz
'''
        bag_of_bones = _build_bag_of_bones(data)
        expected = {
            3: [Token((INDENT, '    ', (3, 0), (3, 4), '    self.assertEqual(foo, bar)\n')),
                Token((NAME, 'self', (3, 4), (3, 8), '    self.assertEqual(foo, bar)\n')),
                Token((OP, '.', (3, 8), (3, 9), '    self.assertEqual(foo, bar)\n')),
                Token((NAME, 'assertEqual', (3, 9), (3, 20), '    self.assertEqual(foo, bar)\n')),
                Token((OP, '(', (3, 20), (3, 21), '    self.assertEqual(foo, bar)\n')),
                Token((NAME, 'foo', (3, 21), (3, 24), '    self.assertEqual(foo, bar)\n')),
                Token((OP, ',', (3, 24), (3, 25), '    self.assertEqual(foo, bar)\n')),
                Token((NAME, 'bar', (3, 26), (3, 29), '    self.assertEqual(foo, bar)\n')),
                Token((OP, ')', (3, 29), (3, 30), '    self.assertEqual(foo, bar)\n')),
                Token((NEWLINE, '\n', (3, 30), (3, 31), '    self.assertEqual(foo, bar)\n'))],
            4: [Token((NAME, 'self', (4, 4), (4, 8), '    self.assertEqual(bat, baz)\n')),
                Token((OP, '.', (4, 8), (4, 9), '    self.assertEqual(bat, baz)\n')),
                Token((NAME, 'assertEqual', (4, 9), (4, 20), '    self.assertEqual(bat, baz)\n')),
                Token((OP, '(', (4, 20), (4, 21), '    self.assertEqual(bat, baz)\n')),
                Token((NAME, 'bat', (4, 21), (4, 24), '    self.assertEqual(bat, baz)\n')),
                Token((OP, ',', (4, 24), (4, 25), '    self.assertEqual(bat, baz)\n')),
                Token((NAME, 'baz', (4, 26), (4, 29), '    self.assertEqual(bat, baz)\n')),
                Token((OP, ')', (4, 29), (4, 30), '    self.assertEqual(bat, baz)\n')),
                Token((NEWLINE, '\n', (4, 30), (4, 31), '    self.assertEqual(bat, baz)\n'))]
        }


        # when
        actual = suppress_mutations(bag_of_bones)

        #
        from pprint import pprint
        print('expected')
        pprint(expected[3])
        print('actual')
        pprint(actual.funcdefs[0].body[3])
        self.assertEqual(expected[3], actual.funcdefs[0].body[3])
        self.assertEqual(expected[4], actual.funcdefs[0].body[4])

    def test_operands_are_extracted_correctly(self):
        # given
        line_tokens = [
            Token((INDENT, '    ', (2, 0), (2, 4), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((NAME, 'foo', (2, 4), (2, 7), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((OP, '(', (2, 7), (2, 8), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((OP, ')', (2, 8), (2, 9), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((OP, '==', (2, 10), (2, 12), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((NAME, 'bar', (2, 13), (2, 16), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((OP, '(', (2, 16), (2, 17), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((NAME, 'bat', (2, 17), (2, 20), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((OP, ',', (2, 20), (2, 21), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((NAME, 'baz', (2, 22), (2, 25), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((OP, '(', (2, 25), (2, 26), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((NAME, 'blabber', (2, 26), (2, 33), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((OP, '=', (2, 33), (2, 34), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((STRING, "'this_is_just_crazy'", (2, 34), (2, 54), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((OP, ')', (2, 54), (2, 55), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((OP, ')', (2, 55), (2, 56), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n")),
            Token((NEWLINE, '\n', (2, 56), (2, 57), "    foo() == bar(bat, baz(blabber='this_is_just_crazy'))\n"))
        ]
        expected_lvalue = line_tokens[1:4]
        expected_rvalue = line_tokens[5:-1]

        # when
        actual_lvalue, actual_rvalue = _extract_operands(line_tokens)

        # then
        self.assertEqual(expected_lvalue, actual_lvalue)
        self.assertEqual(expected_rvalue, actual_rvalue)

    def test_assert_statements_are_built_correctly(self):
        line_num = 2
        indent_size = 4
        lvalue = [Token((NAME, 'foo', (line_num, None), (None, None), ''))]
        rvalue = [
            Token((NAME, 'bar', (2, 11), (2, 14), "    foo == bar(bat='baz')\n")),
            Token((OP, '(', (2, 14), (2, 15), "    foo == bar(bat='baz')\n")),
            Token((NAME, 'bat', (2, 15), (2, 18), "    foo == bar(bat='baz')\n")),
            Token((OP, '=', (2, 18), (2, 19), "    foo == bar(bat='baz')\n")),
            Token((STRING, "'baz'", (2, 19), (2, 24), "    foo == bar(bat='baz')\n")),
            Token((OP, ')', (2, 24), (2, 25), "    foo == bar(bat='baz')\n")),
        ]

        # self.assertEqual(foo, bar(bat='baz'))
        expected = [
            Token((INDENT, '    ', (2, 0), (2, 4), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((NAME, 'self', (2, 4), (2, 8), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((OP, '.', (2, 8), (2, 9), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((NAME, 'assertEqual', (2, 9), (2, 20), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((OP, '(', (2, 20), (2, 21), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((NAME, 'foo', (2, 21), (2, 24), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((OP, ',', (2, 24), (2, 25), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((NAME, 'bar', (2, 26), (2, 29), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((OP, '(', (2, 29), (2, 30), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((NAME, 'bat', (2, 30), (2, 33), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((OP, '=', (2, 33), (2, 34), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((STRING, "'baz'", (2, 34), (2, 39), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((OP, ')', (2, 39), (2, 40), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((OP, ')', (2, 40), (2, 41), "    self.assertEqual(foo,bar(bat='baz'))\n")),
            Token((NEWLINE, '\n', (2, 41), (2, 42), "    self.assertEqual(foo,bar(bat='baz'))\n"))


        ]

        actual = _build_assertEquals_tokens(line_num, indent_size, lvalue, rvalue)

        self.assertEqual(expected, actual)

    def test_nada(self):
        t1 = Token((NAME,'foo',(2, 21),(2, 24),"    self.assertEqual(foo,bar(bat='baz'))\n"))
        t2 = Token((NAME,'foo',(2, 21),(2, 24),"    self.assertEqual(foo,bar(bat='baz'))\n"))


        t3=Token((NAME,'foo',(2, 21),(2, 24),"    self.assertEqual(foo,bar(bat='baz'))\n"))
        t4=Token((NAME,'foo',(2, 21),(2, 24),"    self.assertEqual(foo,bar(bat='baz'))\n"))

        self.assertEqual(t3,t4)

    def test_nothing(self):
        from pprint import pprint

        data = '''\
def blah():
    foo == bar(bat='baz')
'''

        bob = _build_bag_of_bones(data).funcdefs[0]
        pprint(bob.body)
        # for ln_num in bob.body:
        #     pprint(bob.body[ln_num])


def _build_bag_of_bones(data):
    original_tokens = generate_toks(data)
    return parse_tokens(original_tokens)