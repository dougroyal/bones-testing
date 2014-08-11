from tokenize import NEWLINE
from token import DEDENT

from bones.containers.bag_of_bones import BagOfBones
from bones.containers.funcdef import FuncDef


def parse_tokens(tokens):
    bones = BagOfBones()
    tokens = tokens  # set once in parse_tokens, and never change...EVER
    in_funcdef_sig = False  # Used to collect funcdef signature tokens
    in_funcdef_body = False  # ditto, but for funcdef body tokens
    curr_bdd_block = None  # ditto, but for bdd_block tokens.

    for index, tok in enumerate(tokens):
        # new function declaration
        if tok.value == 'def':
            in_funcdef_sig = True
            funcdef = FuncDef()
            funcdef.signature.append(tok)
            bones.funcdefs.append(funcdef)

        elif _is_end_of_funcdef_sig(index, tok, in_funcdef_sig, tokens):
            in_funcdef_sig = False
            in_funcdef_body = True
            _curr_funcdef(bones).signature.append(tok)

        elif _is_end_of_funcdef_body(tok, in_funcdef_body, bones):
            in_funcdef_body = False
            _curr_funcdef(bones).body.add_token(tok)

        elif in_funcdef_sig:
            _curr_funcdef(bones).signature.append(tok)

        elif in_funcdef_body and _is_bdd_block_keyword(tokens, index, tok, bdd_kw='then'):
            curr_bdd_block = _curr_funcdef(bones).then_block
            curr_bdd_block.add_token(tok)

        elif in_funcdef_body and _is_bdd_block_keyword(tokens, index, tok, bdd_kw='where'):
            curr_bdd_block = _curr_funcdef(bones).where_block
            curr_bdd_block.add_token(tok)

        elif _is_end_of_bdd_block(tok, curr_bdd_block):
            curr_bdd_block = None

        elif curr_bdd_block:
            curr_bdd_block.add_token(tok)

        elif in_funcdef_body:
            _curr_funcdef(bones).body.add_token(tok)

        #TODO raise exception on unknown tokens

    return bones


def _is_end_of_funcdef_sig(index, tok, in_funcdef_sig, tokens):
    return in_funcdef_sig and tok.type == NEWLINE and _prev_tok_is_a_colon(index, tokens)


def _is_end_of_funcdef_body(tok, in_funcdef_body, bones):
    if in_funcdef_body and tok.type == DEDENT:
        return _curr_funcdef(bones).closing_dedent_col == tok.start_col


def _is_bdd_block_keyword(tokens, index, tok, bdd_kw):
    return tok.value == bdd_kw and _next_tok_is_a_colon(index, tokens)


def _is_end_of_bdd_block(tok, curr_bdd_block):
    if curr_bdd_block:
        return curr_bdd_block.is_closing_dedent(tok)


def _curr_funcdef(bones):
    return bones.funcdefs[-1]


def _prev_tok_is_a_colon(index, tokens):
    try:
        return tokens[index - 1].value == ':'
    except:
        return False


def _next_tok_is_a_colon(index, tokens):
    try:
        return tokens[index + 1].value == ':'
    except:
        return False

