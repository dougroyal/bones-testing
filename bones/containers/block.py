from collections import OrderedDict
from token import DEDENT


class Block(OrderedDict):
    """
    A container to hold a dictionary of Tokens with helpers.
    Tokens are grouped by line number. -- The dict key is token line number
    """
    def __init__(self):
        super().__init__()

    def add_token(self, tok):
        if tok.line_num not in self:
            self[tok.line_num] = []
        self[tok.line_num].append(tok)

    def is_closing_dedent(self, tok):
        return tok.type == DEDENT and (self.first_line[0].start_col >= tok.start_col)

    @property # TODO DELETEME
    def name_tok(self):
        # A helper to consolidate index-based logic
        return self[1]

    @property
    def first_line(self):
        return next(iter(self.values()))

    @first_line.setter
    def first_line(self, value):

        try:
            first_line_index = next(iter(self.keys()))
        except StopIteration:
            first_line_index = 1

        self[first_line_index] = value

    @property
    def last_line(self):
        return next(iter(self.values()))

    def lines(self):
        """
        :return: A list of tokens sorted and grouped by line number
        """
        return [self[key] for key in sorted(self.keys())]