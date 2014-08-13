from token import INDENT, NAME, OP, STRING, NEWLINE
from unittest import TestCase
from bones.containers.bones_token import Token
from bones.utils.builder import build_line


class TestBuilder(TestCase):

    def test_line_should_be_built_from_tokens(self):
        line = [
            Token((INDENT, '    ', (3, 0), (3, 4), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((NAME, 'self', (3, 4), (3, 8), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((OP, '.', (3, 8), (3, 9), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((NAME, 'assertEqual', (3, 9), (3, 20), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((OP, '(', (3, 20), (3, 21), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((NAME, 'foo', (3, 21), (3, 24), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((OP, ',', (3, 24), (3, 25), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((NAME, 'bar', (3, 26), (3, 29), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((OP, '(', (3, 29), (3, 30), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((NAME, 'bat', (3, 30), (3, 33), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((OP, '=', (3, 33), (3, 34), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((STRING, "'baz'", (3, 34), (3, 39), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((OP, ')', (3, 39), (3, 40), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((OP, ')', (3, 40), (3, 41), "    self.assertEqual(foo, bar(bat='baz'))\n")),
            Token((NEWLINE,'\n',(3, 41),(3, 42),"    self.assertEqual(foo, bar(bat='baz'))\n"))
        ]

        actual = build_line(line)

        self.assertEqual("    self.assertEqual(foo,bar(bat='baz'))\n", actual)