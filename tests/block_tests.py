from io import StringIO
from pprint import pprint
from token import DEDENT
import unittest
from unittest import TestCase

from bones.containers.block import Block
from bones.tokengenerator import generate_tokens
from tests.utils import mk_tok

LINE_ZERO = 0
LINE_ONE = 1


class BlockTests(TestCase):

    def test_tokens_are_added_by_line_number(self):
        # given
        block = Block()

        tok_0_0 = mk_tok(line=LINE_ZERO)
        tok_0_1 = mk_tok(line=LINE_ZERO)
        tok_0_2 = mk_tok(line=LINE_ZERO)
        tok_1_0 = mk_tok(line=LINE_ONE)
        tok_1_1 = mk_tok(line=LINE_ONE)
        tok_1_2 = mk_tok(line=LINE_ONE)

        # when
        block.add_token(tok_0_0)
        block.add_token(tok_0_1)
        block.add_token(tok_0_2)
        block.add_token(tok_1_0)
        block.add_token(tok_1_1)
        block.add_token(tok_1_2)

        # then
        self.assertEqual(tok_0_0, block[LINE_ZERO][0])
        self.assertEqual(tok_0_1, block[LINE_ZERO][1])
        self.assertEqual(tok_0_2, block[LINE_ZERO][2])

        self.assertEqual(tok_1_0, block[LINE_ONE][0])
        self.assertEqual(tok_1_1, block[LINE_ONE][1])
        self.assertEqual(tok_1_2, block[LINE_ONE][2])

    def test_high_line_number_tokens_are_added_correctly(self):
        block = Block()
        tok0 = mk_tok(line=100)
        tok1 = mk_tok(line=100)

        block.add_token(tok0)
        block.add_token(tok1)

        self.assertEqual(block[100][0], tok0)
        self.assertEqual(block[100][1], tok1)

    def test_block_dedent_is_identified_correctly(self):
        block = Block()

        data='''\
def somefunc():
    if not_the_real_dedent:
        pass
    add_some_dedent_confusion = 42
'''
        tokens = generate_tokens(StringIO(data))
        dedents = _find_dedent_tokens(tokens)
        for tok in tokens:
            block.add_token(tok)

        self.assertEqual(False, block.is_closing_dedent(dedents[0]))
        self.assertEqual(True, block.is_closing_dedent(dedents[1]))


def _find_dedent_tokens(tokens):
    return [tok for tok in tokens if tok.type == DEDENT]

if __name__ == '__main__':
    unittest.main()
