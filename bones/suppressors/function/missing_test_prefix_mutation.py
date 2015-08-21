from token import NAME
from tokenize import TokenInfo

from bones.suppressors.known_mutants import BDD_BLOCK

DEF_TOKEN_POSITION=0
FUNC_NAME_TOKEN_POSITION=1


def is_found(block):
    return any(BDD_BLOCK == b.block_type for b in block.children)


def suppress(block):
    tok = block.tokens[1]

    new_func_name = 'test_' + tok.string

    block.tokens[1] = TokenInfo(type=NAME, string=new_func_name, start=tok.start, end=tok.end, line=tok.line)

    return block
