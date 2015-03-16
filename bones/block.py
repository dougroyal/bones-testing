from token import INDENT, DEDENT

# available block_types
MODULE = 'module'
CLASS = 'class'
FUNCTION = 'function'
BDD_BLOCK = 'bdd_block'

BDD_BLOCK_TYPES = ['given', 'when', 'then']


class Block():
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