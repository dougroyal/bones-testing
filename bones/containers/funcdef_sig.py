

class FuncDefSig(list):

    @property
    def name_tok(self):
        # A helper to consolidate index-based logic
        return self[1]