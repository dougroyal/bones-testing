from token import INDENT

from bones.containers.funcdef_sig import FuncDefSig

class FuncDef():

    def __init__(self):
        self._closing_dedent_col = None
        self.signature = FuncDefSig()
        # todo make body an object like FuncDefSig so I can call fn.body.line(4) rather than fn.body[4]
        self.body = {}
        self.bdd_blocks = {'then': {},
                           'where': {}}

    def add_body_token(self, tok):
        if tok.line_num not in self.body:
            self.body[tok.line_num] = []
        self.body[tok.line_num].append(tok)

    def add_bdd_token(self, part, tok):
        if tok.line_num not in self.bdd_blocks[part]:
            self.bdd_blocks[part][tok.line_num] = []
        self.bdd_blocks[part][tok.line_num].append(tok)

    @property
    def closing_dedent_col(self):
        # If the first indent block has already been found, return that.
        if self._closing_dedent_col:
            return self._closing_dedent_col

        # Find the first indent token, save its value, and return that value
        for key in self.body:
            if self.body[key][0].type == INDENT:
                self._closing_dedent_col = self.body[key][0].start[1]
                return self._closing_dedent_col