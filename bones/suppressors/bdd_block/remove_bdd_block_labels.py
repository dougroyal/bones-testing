from token import NAME
from tokenize import TokenInfo, COMMENT

from bones.suppressors.known_mutants import BDD_BLOCK_TYPES


def is_found(block):
    return (len(block.tokens) > 0
            and block.tokens[0].type == NAME
            and block.tokens[0].string in BDD_BLOCK_TYPES)


def suppress(block):
    # the first three tokens are a NAME, and OP,and a NEWLINE.
    # just comment them out
    block.tokens[0] = _make_comment_token(block.tokens[0])
    return block


def _make_comment_token(tok):
    return TokenInfo(COMMENT, '#'+tok.string, tok.start, tok.end, tok.line)

