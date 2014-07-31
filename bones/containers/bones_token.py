from token import tok_name

class Token():
    """
    A wrapper, similar to the TokenInfo class in python 3.2+
    to make working with tokens easier when using 3.0 and 3.1

    Also has a few other properties to simplify accessing extra metadata.
    """


    def __init__(self, args):
        self.type = args[0]
        self.value = args[1]
        self.start = args[2]
        self.end = args[3]
        self.line = args[4]

        # Add extra stuff to make life more fun
        self.line_num = self.start[0]
        self.start_col = self.start[1]

    def __repr__(self):
        # print something that can be used in tests
        return 'Token(({},{!r},{!r},{!r},{!r})),'.format(tok_name[self.type], self.value, self.start, self.end, self.line)

    def __eq__(self, other):
        # results = [self.__dict__[member] != other.__dict__[member] for member in self.__dict__.keys()]

        if not isinstance(other, Token):
            raise TypeError('not a Token: ' + str(other))

        for member in self.__dict__.keys():
            if self.__dict__[member] != other.__dict__[member]:
                return False
        return True

