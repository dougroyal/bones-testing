from tokenize import NEWLINE
from token import DEDENT

from bones.containers.bag_of_bones import BagOfBones
from bones.containers.funcdef import FuncDef


def parse_tokens(tokens):
    bones = BagOfBones()
    in_funcdef_body = False  # ditto, but for funcdef body tokens
    curr_bdd_block = None  # ditto, but for bdd_block tokens.

    for index, tok in enumerate(tokens):
        # new function declaration
        if tok.value == 'def':
            in_funcdef_body = True
            funcdef = FuncDef()
            funcdef.add_token(tok)
            bones.funcdefs.append(funcdef)
            _curr_funcdef(bones).body.add_token(tok)

        elif in_funcdef_body and _is_end_of_funcdef_body(tok, bones):
            in_funcdef_body = False
            _curr_funcdef(bones).body.add_token(tok)

        elif in_funcdef_body and _is_bdd_block_keyword(tokens, index, tok, bdd_kw='then'):
            curr_bdd_block = _curr_funcdef(bones).then_block
            curr_bdd_block.add_token(tok)

        elif in_funcdef_body and _is_bdd_block_keyword(tokens, index, tok, bdd_kw='where'):
            curr_bdd_block = _curr_funcdef(bones).where_block
            curr_bdd_block.add_token(tok)

        elif curr_bdd_block and curr_bdd_block.is_closing_dedent(tok):
            curr_bdd_block = None

        elif curr_bdd_block:
            curr_bdd_block.add_token(tok)

        elif in_funcdef_body:
            _curr_funcdef(bones).body.add_token(tok)

        else:
            bones.module.add_token(tok)

    return bones


def _is_end_of_funcdef_sig(tokens, index, tok):
    return tok.type == NEWLINE and _prev_tok_is_a_colon(tokens, index)


def _is_end_of_funcdef_body(tok, bones):
    return (tok.type == DEDENT) and (_curr_funcdef(bones).closing_dedent_col == tok.start_col)


def _is_bdd_block_keyword(tokens, index, tok, bdd_kw):
    return tok.value == bdd_kw and _next_tok_is_a_colon(tokens, index)


def _is_end_of_bdd_block(tok, curr_bdd_block):
    if curr_bdd_block:
        return curr_bdd_block.is_closing_dedent(tok)


def _curr_funcdef(bones):
    return bones.funcdefs[-1]


def _prev_tok_is_a_colon(tokens, index):
    try:
        return tokens[index - 1].value == ':'
    except:
        return False


def _next_tok_is_a_colon(tokens, index):
    try:
        return tokens[index + 1].value == ':'
    except:
        return False

