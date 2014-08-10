from token import STRING
from bones.containers.bones_token import Token


def mk_tok(line):
    return Token((STRING, '', (line, 0), (0, 0), ''))
