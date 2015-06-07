from token import NAME

from bones.suppressors.known_mutants import BDD_BLOCK_TYPES


def is_found(block):
    return block.tokens[0].type == NAME and block.tokens[0].string in BDD_BLOCK_TYPES


def suppress(block):

    # the first three tokens are a NAME, and OP,and a NEWLINE, so just remove them.
    block.tokens = block.tokens[3:]
    return block

