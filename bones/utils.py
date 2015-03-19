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


def print_tokens(file_content):
    tokens = generate_tokens(io.StringIO(file_content).readline)
    pprint([t for t in tokens])

if __name__ == '__main__':
    print_tokens('''def "a sexy test string function definition"():
    pass
''')