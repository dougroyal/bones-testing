

class FuncDefSig(list):
    #TODO if funcdef were are Block, a signature would simply be the first line of the block ... so do that.

    @property
    def name_tok(self):
        # A helper to consolidate index-based logic
        return self[1]