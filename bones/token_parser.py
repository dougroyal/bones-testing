from tokenize import NEWLINE
from token import DEDENT

from bones.containers.bag_of_bones import BagOfBones
from bones.containers.funcdef import FuncDef

from pprint import pprint

#todo maybe de-classify this
class TokenParser:

    def __init__(self):
        self._bones = BagOfBones()
        self._tokens = None  # set once in parse_tokens, and never change...EVER
        self._in_funcdef_sig = False  # Used to collect funcdef signature tokens
        self._in_funcdef_body = False  # ditto, but for funcdef body tokens

        self._curr_bdd_block = None  # ditto, but for bdd_block tokens. Will contain bdd_keywords: 'then', 'when', etc

    def parse_tokens(self, tokens):
        self._tokens = tokens

        for index, tok in enumerate(tokens):
            # new function declaration
            if tok.value == 'def':
                self._in_funcdef_sig = True

                funcdef = FuncDef()
                funcdef.signature.append(tok)
                self._bones.funcdefs.append(funcdef)

            elif self._is_end_of_funcdef_sig(index, tok):
                self._in_funcdef_sig = False
                self._in_funcdef_body = True
                self._curr_funcdef().signature.append(tok)

            elif self._is_end_of_funcdef_body(tok):
                self._in_funcdef_body = False
                self._curr_funcdef().body.add_token(tok)

            elif self._in_funcdef_sig:
                self._curr_funcdef().signature.append(tok)

            elif self._is_bdd_block_keyword(index, tok, bdd_kw='then'):
                self._curr_bdd_block = 'then'
                self._curr_funcdef().then_block.add_token(tok)

            elif self._is_bdd_block_keyword(index, tok, bdd_kw='where'):
                self._curr_bdd_block = 'where'
                self._curr_funcdef().add_bdd_token('where', tok)

            elif self._is_end_of_bdd_block(tok):
                self._curr_bdd_block = None

            elif self._curr_bdd_block == 'then':
                self._curr_funcdef().then_block.add_token(tok)

            elif self._curr_bdd_block == 'where':
                self._curr_funcdef().where_block.add_token(tok)

            elif self._in_funcdef_body:
                self._curr_funcdef().body.add_token(tok)

            #TODO raise exception on unknown tokens

        return self._bones


    def _is_end_of_funcdef_sig(self, index, tok):
        return self._in_funcdef_sig and tok.type == NEWLINE and self._prev_tok_is_a_colon(index)

    def _is_end_of_funcdef_body(self, tok):
        if self._in_funcdef_body and tok.type == DEDENT:
            return self._curr_funcdef().closing_dedent_col == tok.start_col

    def _is_bdd_block_keyword(self, index, tok, bdd_kw):
        return self._in_funcdef_body and tok.value == bdd_kw and self._next_tok_is_a_colon(index)

    def _is_end_of_bdd_block(self, tok):
        if self._curr_bdd_block and tok.type == DEDENT:
            lowest_line, *rest = self._curr_funcdef().bdd_blocks[self._curr_bdd_block]
            block_start_col = self._curr_funcdef().bdd_blocks[self._curr_bdd_block][lowest_line][0].start_col
            return block_start_col >= tok.start_col  # The DEDENT might go all the way to 0

    def _curr_funcdef(self):
        return self._bones.funcdefs[-1]

    def _prev_tok_is_a_colon(self, index):
        try:
            return self._tokens[index - 1].value == ':'
        except:
            return False

    def _next_tok_is_a_colon(self, index):
        try:
            return self._tokens[index + 1].value == ':'
        except:
            return False

