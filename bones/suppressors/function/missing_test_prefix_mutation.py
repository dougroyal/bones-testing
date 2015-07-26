from token import NAME
from tokenize import TokenInfo

from bones.suppressors.known_mutants import BDD_BLOCK

DEF_TOKEN_POSITION=0
FUNC_NAME_TOKEN_POSITION=1


def is_found(block):
    return any(BDD_BLOCK == b.block_type for b in block.children)


def suppress(block):
    tok = block.tokens[1]

    old_func_name = tok.string
    new_func_name = 'test_' + tok.string

    block.tokens[1] = TokenInfo(type=NAME, string=new_func_name, start=tok.start, end=tok.end, line=tok.line)

    for index, tok in enumerate(block.tokens):
        block.tokens[index] = _build_token_with_updated_line_value(index, tok, old_func_name, new_func_name)

    return block


def _build_token_with_updated_line_value(index, tok, old_func_name, new_func_name):

    new_line = tok.line.replace(old_func_name, new_func_name)

    if index == DEF_TOKEN_POSITION:
        # The def token won't be shifted to the left because it comes before the function name.
        start_left_shift_amount = 0
        end_left_shift_amount = 0
    elif index == FUNC_NAME_TOKEN_POSITION:
        # The func_name start wont change, but the end will
        start_left_shift_amount = 0
        end_left_shift_amount = 5
    else:
        # -2 from column because we removed two quotes (")
        start_left_shift_amount = 5
        end_left_shift_amount = 5

    # tok.start[0] and tok.end[0] is the _line_ number
    # tok.start[1] and tok.end[1] is the _column_ number
    new_start = (tok.start[0],  int(tok.start[1]) + start_left_shift_amount)
    new_end = (tok.end[0], int(tok.end[1]) + end_left_shift_amount)

    return TokenInfo(type=tok.type, string=tok.string, start=new_start, end=new_end, line=new_line)

