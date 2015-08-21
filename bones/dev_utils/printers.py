"""
Utility functions to help _develop_ bones.
"""
import io
from tokenize import generate_tokens
from pprint import pprint


def print_bones(block):
    print('\n%s'%block.block_type.upper())
    for tok in block.tokens:
        print("\t"+str(tok))

    for child in block.children:
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