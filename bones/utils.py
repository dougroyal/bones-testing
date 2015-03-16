"""
Utility functions to help _develop_ bones.
"""


def print_bones(block):
    for child in block.children:
        print(child.block_type)

        for tok in child.tokens:
            print("\t"+str(tok))

        print_bones(child)
