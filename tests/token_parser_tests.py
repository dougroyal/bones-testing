import unittest
from unittest import TestCase
from token import NAME, OP, STRING, NEWLINE, INDENT, DEDENT, NUMBER

from bones.containers.bones_token import Token
from bones.token_parser import parse_tokens

from tests.utils import generate_toks

class TokenParserTests(TestCase):

    def test_normal_funcdef_signature_is_parsed_correctly(self):
        data = '''\
def something(foo, bar="baz", bat=metasyntactic_generator()):
    pass
'''
        tokens = generate_toks(data)

        expected = [
            Token((NAME, 'def', (1, 0), (1, 3), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((NAME, 'something', (1, 4), (1, 13), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((OP, '(', (1, 13), (1, 14), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((NAME, 'foo', (1, 14), (1, 17), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((OP, ',', (1, 17), (1, 18), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((NAME, 'bar', (1, 19), (1, 22), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((OP, '=', (1, 22), (1, 23), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((STRING, '"baz"', (1, 23), (1, 28), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((OP, ',', (1, 28), (1, 29), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((NAME, 'bat', (1, 30), (1, 33), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((OP, '=', (1, 33), (1, 34), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((NAME, 'metasyntactic_generator', (1, 34), (1, 57), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((OP, '(', (1, 57), (1, 58), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((OP, ')', (1, 58), (1, 59), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((OP, ')', (1, 59), (1, 60), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((OP, ':', (1, 60), (1, 61), 'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
            Token((NEWLINE, '\n', (1, 61), (1, 62),'def something(foo, bar="baz", bat=metasyntactic_generator()):\n')),
        ]

        parsed = parse_tokens(tokens)

        self.assertEqual(len(expected), len(parsed.funcdefs[0].signature))
        for i, expect in enumerate(expected):
            self.assertEqual(expected[i], parsed.funcdefs[0].signature[i])


    def test_string_funcdef_signature_is_parsed_correctly(self):
        # given
        data = '''\
def "a cool string func"(a,b=c,d="e",f=g()):
    pass
'''
        tokens = generate_toks(data)

        expected = [
            Token((NAME, 'def', (1, 0), (1, 3), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((STRING, '"a cool string func"', (1, 4), (1, 24), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, '(', (1, 24), (1, 25), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((NAME, 'a', (1, 25), (1, 26), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, ',', (1, 26), (1, 27), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((NAME, 'b', (1, 27), (1, 28), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, '=', (1, 28), (1, 29), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((NAME, 'c', (1, 29), (1, 30), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, ',', (1, 30), (1, 31), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((NAME, 'd', (1, 31), (1, 32), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, '=', (1, 32), (1, 33), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((STRING, '"e"', (1, 33), (1, 36), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, ',', (1, 36), (1, 37), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((NAME, 'f', (1, 37), (1, 38), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, '=', (1, 38), (1, 39), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((NAME, 'g', (1, 39), (1, 40), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, '(', (1, 40), (1, 41), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, ')', (1, 41), (1, 42), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, ')', (1, 42), (1, 43), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((OP, ':', (1, 43), (1, 44), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
            Token((NEWLINE, '\n', (1, 44), (1, 45), 'def "a cool string func"(a,b=c,d="e",f=g()):\n')),
        ]

        # when
        parsed = parse_tokens(tokens)

        # then
        self.assertEqual(expected, parsed.funcdefs[0].signature)

    def test_tokens_are_parsed_into_funcdef_body(self):
        # given
        data = '''\
def somefunc():

    foo = some_other_func_call()
'''
        expected_line_2 = [Token((55, '\n', (2, 0), (2, 1), '\n')),]
        expected_line_3 = [
            Token((INDENT, '    ', (3, 0), (3, 4), '    foo = some_other_func_call()\n')),
            Token((NAME, 'foo', (3, 4), (3, 7), '    foo = some_other_func_call()\n')),
            Token((OP, '=', (3, 8), (3, 9), '    foo = some_other_func_call()\n')),
            Token((NAME, 'some_other_func_call', (3, 10), (3, 30), '    foo = some_other_func_call()\n')),
            Token((OP, '(', (3, 30), (3, 31), '    foo = some_other_func_call()\n')),
            Token((OP, ')', (3, 31), (3, 32), '    foo = some_other_func_call()\n')),
            Token((NEWLINE, '\n', (3, 32), (3, 33), '    foo = some_other_func_call()\n')),
        ]
        expected_line_4 = [Token((DEDENT, '', (4, 0), (4, 0), ''))]
        tokens = generate_toks(data)

        # when
        parsed = parse_tokens(tokens)

        # then
        # line 2 Token tests
        actual_line_2 = parsed.funcdefs[0].body[2]
        self.assertEqual(expected_line_2, actual_line_2)

        # line 3 Token tests
        actual_line_3 = parsed.funcdefs[0].body[3]
        self.assertEqual(expected_line_3, actual_line_3)

        # line 4 Token tests
        actual_line_4 = parsed.funcdefs[0].body[4]
        self.assertEqual(expected_line_4, actual_line_4)

    def test_bdd_keywords_are_parsed_into_funcdef_parts(self):
        # given
        data = '''\
def somefunc():
    this_should_not_be_found_in_a_bdd_block()

    then:
        a == b
'''
        LINE_FOUR = 4
        LINE_FIVE = 5

        expected_line_4 = [
            Token((NAME,'then', (LINE_FOUR, 4), (4, 8), '    then:\n')),
            Token((OP, ':', (LINE_FOUR, 8), (4, 9), '    then:\n')),
            Token((NEWLINE, '\n', (LINE_FOUR, 9), (4, 10), '    then:\n')),
        ]
        expected_line_5 = [
            Token((INDENT, '        ', (LINE_FIVE, 0), (5, 8), '        a == b\n')),
            Token((NAME, 'a', (LINE_FIVE, 8), (5, 9), '        a == b\n')),
            Token((OP, '==', (LINE_FIVE, 10), (5, 12), '        a == b\n')),
            Token((NAME, 'b', (LINE_FIVE, 13), (5, 14), '        a == b\n')),
            Token((NEWLINE, '\n', (LINE_FIVE, 14),(5, 15),'        a == b\n')),
        ]
        tokens = generate_toks(data)

        # when
        parsed = parse_tokens(tokens)

        # then
        actual_line_4 = parsed.funcdefs[0].then_block[LINE_FOUR]
        actual_line_5 = parsed.funcdefs[0].then_block[LINE_FIVE]

        self.assertEqual(expected_line_4, actual_line_4)
        self.assertEqual(expected_line_5, actual_line_5)

    def test_tables_are_parsed_into_funcdef_parts(self):
        data = '''\
def somefunc():

    then:
        max(a, b) == c

    where:
        a | b | c
        1 | 2 | 2
        3 | 4 | 4
'''
        expected = [
            Token((NAME, 'where', (6, 4), (6, 9), '    where:\n')),
            Token((OP, ':', (6, 9), (6, 10), '    where:\n')),
            Token((NEWLINE, '\n', (6, 10), (6, 11), '    where:\n')),
            Token((INDENT, '        ', (7, 0), (7, 8), '        a | b | c\n')),
            Token((NAME, 'a', (7, 8), (7, 9), '        a | b | c\n')),
            Token((OP, '|', (7, 10), (7, 11), '        a | b | c\n')),
            Token((NAME, 'b', (7, 12), (7, 13), '        a | b | c\n')),
            Token((OP, '|', (7, 14), (7, 15), '        a | b | c\n')),
            Token((NAME, 'c', (7, 16), (7, 17), '        a | b | c\n')),
            Token((NEWLINE, '\n', (7, 17), (7, 18), '        a | b | c\n')),
            Token((NUMBER, '1', (8, 8), (8, 9), '        1 | 2 | 2\n')),
            Token((OP, '|', (8, 10), (8, 11), '        1 | 2 | 2\n')),
            Token((NUMBER, '2', (8, 12), (8, 13), '        1 | 2 | 2\n')),
            Token((OP, '|', (8, 14), (8, 15), '        1 | 2 | 2\n')),
            Token((NUMBER, '2', (8, 16), (8, 17), '        1 | 2 | 2\n')),
            Token((NEWLINE, '\n', (8, 17), (8, 18), '        1 | 2 | 2\n')),
            Token((NUMBER, '3', (9, 8), (9, 9), '        3 | 4 | 4\n')),
            Token((OP, '|', (9, 10), (9, 11), '        3 | 4 | 4\n')),
            Token((NUMBER, '4', (9, 12), (9, 13), '        3 | 4 | 4\n')),
            Token((OP, '|', (9, 14), (9, 15), '        3 | 4 | 4\n')),
            Token((NUMBER, '4', (9, 16), (9, 17), '        3 | 4 | 4\n')),
            Token((NEWLINE, '\n', (9, 17), (9, 18),'        3 | 4 | 4\n')),
        ]

        tokens = generate_toks(data)

        parsed = parse_tokens(tokens)

        line_6_toks = parsed.funcdefs[0].where_block[6]
        line_7_toks = parsed.funcdefs[0].where_block[7]
        line_8_toks = parsed.funcdefs[0].where_block[8]
        line_9_toks = parsed.funcdefs[0].where_block[9]


        # Line 3 Token tests
        self.assertEqual(3, len(line_6_toks))
        self.assertEqual(expected[0], line_6_toks[0])
        self.assertEqual(expected[1], line_6_toks[1])
        self.assertEqual(expected[2], line_6_toks[2])

        # Line 7 Token tests
        self.assertEqual(7, len(line_7_toks))
        self.assertEqual(expected[3], line_7_toks[0])
        self.assertEqual(expected[4], line_7_toks[1])
        self.assertEqual(expected[5], line_7_toks[2])
        self.assertEqual(expected[6], line_7_toks[3])
        self.assertEqual(expected[7], line_7_toks[4])
        self.assertEqual(expected[8], line_7_toks[5])
        self.assertEqual(expected[9], line_7_toks[6])

        # Line 8 Token tests
        self.assertEqual(6, len(line_8_toks))
        self.assertEqual(expected[10], line_8_toks[0])
        self.assertEqual(expected[11], line_8_toks[1])
        self.assertEqual(expected[12], line_8_toks[2])
        self.assertEqual(expected[13], line_8_toks[3])
        self.assertEqual(expected[14], line_8_toks[4])
        self.assertEqual(expected[15], line_8_toks[5])

        # Line 9 Token tests
        self.assertEqual(6, len(line_9_toks))
        self.assertEqual(expected[16], line_9_toks[0])
        self.assertEqual(expected[17], line_9_toks[1])
        self.assertEqual(expected[18], line_9_toks[2])
        self.assertEqual(expected[19], line_9_toks[3])
        self.assertEqual(expected[20], line_9_toks[4])
        self.assertEqual(expected[21], line_9_toks[5])


if __name__ == '__main__':
    unittest.main()
