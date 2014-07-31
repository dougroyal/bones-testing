import unittest

from bones.containers.funcdef import FuncDef
from bones.tokengenerator import Token


def mk_tok(line):
    return Token((None, None, (line, None), (None, None), None))


class FuncDefTests(unittest.TestCase):

    def test_tokens_are_added_to_body(self):
        funcdef = FuncDef()
        line0_tok0 = mk_tok(line=0)
        line0_tok1 = mk_tok(line=0)
        line1_tok0 = mk_tok(line=1)
        line1_tok1 = mk_tok(line=1)

        funcdef.add_body_token(line0_tok0)
        funcdef.add_body_token(line0_tok1)
        funcdef.add_body_token(line1_tok0)
        funcdef.add_body_token(line1_tok1)

        self.assertEqual(funcdef.body[0][0], line0_tok0)
        self.assertEqual(funcdef.body[0][1], line0_tok1)
        self.assertEqual(funcdef.body[1][0], line1_tok0)
        self.assertEqual(funcdef.body[1][1], line1_tok1)

    def test_high_line_number_tokens_are_added_correctly(self):
        funcdef = FuncDef()
        tok0 = mk_tok(line=100)
        tok1 = mk_tok(line=100)

        funcdef.add_body_token(tok0)
        funcdef.add_body_token(tok1)

        self.assertEqual(funcdef.body[100][0], tok0)
        self.assertEqual(funcdef.body[100][1], tok1)

    def test_bdd_tokens_are_added_to_correct_block(self):
        funcdef = FuncDef()
        tok0 = mk_tok(line=0)
        tok1 = mk_tok(line=0)
        tok2 = mk_tok(line=0)

        # THEN
        funcdef.add_bdd_token('then', tok0)
        funcdef.add_bdd_token('then', tok1)
        funcdef.add_bdd_token('then', tok2)

        self.assertEqual(funcdef.bdd_blocks['then'][0][0], tok0)
        self.assertEqual(funcdef.bdd_blocks['then'][0][1], tok1)
        self.assertEqual(funcdef.bdd_blocks['then'][0][2], tok2)

        # WHERE
        funcdef.add_bdd_token('where', tok0)
        funcdef.add_bdd_token('where', tok1)
        funcdef.add_bdd_token('where', tok2)

        self.assertEqual(funcdef.bdd_blocks['where'][0][0], tok0)
        self.assertEqual(funcdef.bdd_blocks['where'][0][1], tok1)
        self.assertEqual(funcdef.bdd_blocks['where'][0][2], tok2)


if __name__ == '__main__':
    unittest.main()
