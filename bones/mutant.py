from token import INDENT, DEDENT

# known mutants
MODULE = 'module'
CLASS = 'class'
FUNCTION = 'function'
BDD_BLOCK = 'bdd_block'

BDD_BLOCK_TYPES = ['given', 'when', 'then']

# This is a simply a node in a tree...mutant sounded more fun.
class Mutant:
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