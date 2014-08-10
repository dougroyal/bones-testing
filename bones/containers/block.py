from collections import OrderedDict
from token import DEDENT


class Block(OrderedDict):
    """
    A container to hold a ordered dictionary of Tokens with helpers.
    Tokens are grouped by line number. -- the dict key is token line number
    """

    def add_token(self, tok):
        if tok.line_num not in self:
            self[tok.line_num] = []
        self[tok.line_num].append(tok)

    def is_closing_dedent(self, tok):
        return tok.type == DEDENT and (self.first_line[0].start_col >= tok.start_col)
    
    @property
    def first_line(self):
        return next(iter(self.values()))

