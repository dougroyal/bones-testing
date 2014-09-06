from token import DEDENT


class Block(dict):
    """
    A container to hold a dictionary of Tokens with helpers.
    Tokens are grouped by line number. -- The dict key is token line number
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

    def lines(self):
        """
        :return: A list of tokens sorted and grouped by line number
        """
        return [self[key] for key in sorted(self.keys())]