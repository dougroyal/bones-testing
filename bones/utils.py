"""
Utility functions to help _develop_ bones.
"""
import io
from tokenize import generate_tokens
from pprint import pprint


def print_bones(block):
    for child in block.children:
        print(child.block_type)

        for tok in child.tokens:
            print("\t"+str(tok))

        print_bones(child)


def tokens_from_string(s):
    return generate_tokens(io.StringIO(s).readline)


def print_tokens(file_content):
    tokens = tokens_from_string(file_content)
    pprint(list(tokens))

if __name__ == '__main__':
    print_tokens('''def "a sexy test string function definition"():
    pass
''')