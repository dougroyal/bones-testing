from token import INDENT, DEDENT
from tokenize import TokenInfo


class BonesNode:
    def __init__(self, block_type, parent):
        self.parent = parent
        self.children = []  # classes, functions, and BDD blocks
        self.block_type = block_type  # MODULE, CLASS, FUNCTION, OR BDD_BLOCK
        self.tokens = []

        self._indent_count = 0

    def is_my_dedent(self, tok):
        if tok.type == DEDENT and self._indent_count is not 0:
            self._indent_count -= 1

            if self._indent_count == 0:
                return True

        if tok.type == INDENT:
            self._indent_count += 1

        return False

    def __str__(self):
        import pprint
        return 'BonesNode Type: {type}\nTokens: {tokens}'.format(type=self.block_type,
                                                              tokens=pprint.pformat(self.tokens))


def fix_line_numbers(bones_tokens: list) -> list:
    """
    :param bones_tokens: A list of TokenItem where the line numbers may not be in order.
    :return: A list of TokenItem where the line numbers are in order starting with 1.
    """
    return [_create_token(index+1, tok) for index, tok in enumerate(bones_tokens)]


def _create_token(index, tok):
    start = (index, tok.start[1])
    end = (index, tok.end[1])
    return TokenInfo(tok.type, tok.string, start, end, tok.line)

def flatten(bones_tree):
    # The ENDMARKER needs to be at the end, so append the root tokens to flattened tokens.
    root_tokens = bones_tree.tokens
    bones_tree.tokens = []
    tokens = _flatten(bones_tree)
    tokens.extend(root_tokens)

    return tokens


def _flatten(bones_tree):
    tokens = bones_tree.tokens
    for child in bones_tree.children:
        tokens.extend(_flatten(child))
    return tokens

