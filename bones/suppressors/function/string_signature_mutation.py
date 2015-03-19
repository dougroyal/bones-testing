from token import STRING, NAME
import re
from tokenize import TokenInfo

INVALID_NAME_CHARS_PATTERN = re.compile(r'[^0-9a-zA-Z_]+')


def is_found(block):
    return block.tokens[1].type == STRING


def suppress(block):
    tok = block.tokens[1]

    func_name = tok.string[1:-1]  # strip quotes from string ... this is why order of suppression is important.
    func_name = re.sub(INVALID_NAME_CHARS_PATTERN, '_', func_name)

    block.tokens[1] = TokenInfo(type=NAME, string=func_name, start=tok.start, end=tok.end, line=tok.line)

    return block

