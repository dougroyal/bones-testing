from token import INDENT

from bones.containers.block import Block


class FuncDef(Block):

    def __init__(self):
        super().__init__()
        self._closing_dedent_col = None
        self.body = Block()
        self.then_block = Block()
        self.where_block = Block()

    @property
    def closing_dedent_col(self):
        # If the first indent block has already been found, return that.
        if self._closing_dedent_col:
            return self._closing_dedent_col

        # Find the first indent token, save the start column value, and return that value
        for key in self.body:
            if self.body[key][0].type == INDENT:
                self._closing_dedent_col = self.body[key][0].start[1]
                return self._closing_dedent_col