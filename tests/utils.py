from token import STRING
from io import StringIO

from tokenize import generate_tokens

from bones.containers.bones_token import Token


def mk_tok(line):
    return Token((STRING, '', (line, 0), (0, 0), ''))


def generate_toks(data):
    return [Token(t) for t in generate_tokens(StringIO(data).readline)]
