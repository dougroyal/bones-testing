from token import INDENT, DEDENT


class BonesNode:
    def __init__(self, block_type, parent):
        self.parent = parent
        self.children = []  # classes, functions, and BDD blocks
        self.block_type = block_type  # MODULE, CLASS, FUNCTION, OR BDD_BLOCK
        self.tokens = []

        self._indents = 0

    def is_my_dedent(self, tok):
        if tok.type == DEDENT:
            self._indents -= 1

            if self._indents == 0:
                return True

        if tok.type == INDENT:
            self._indents += 1

        return False

    def __str__(self):
        import pprint
        return 'BonesNode Type: {type}\nTokens: {tokens}'.format(type=self.block_type,
                                                              tokens=pprint.pformat(self.tokens))