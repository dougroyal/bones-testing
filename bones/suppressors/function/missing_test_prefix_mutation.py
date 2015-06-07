from token import NAME
from tokenize import TokenInfo

from bones.suppressors.known_mutants import BDD_BLOCK


def is_found(block):
    return any(BDD_BLOCK == b.block_type for b in block.children)


def suppress(block):
    tok = block.tokens[1]

    func_name = 'test_' + tok.string

    block.tokens[1] = TokenInfo(type=NAME, string=func_name, start=tok.start, end=tok.end, line=tok.line)

    return block

