from token import INDENT, DEDENT


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


def flatten(bones_tree):
    tokens = bones_tree.tokens
    for child in bones_tree.children:
        tokens.extend(flatten(child))

    # Sort tokens based on their original line number (start[0]), and their column (end[1]) on that line.
    return sorted(tokens, key=lambda tok: (tok.start[0], tok.end[1]))