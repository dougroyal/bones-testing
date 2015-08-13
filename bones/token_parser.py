from token import NAME

from bones.bones_tree import BonesNode
from bones.suppressors.known_mutants import MODULE, CLASS, FUNCTION, BDD_BLOCK, BDD_BLOCK_TYPES


def parse(tokens) -> BonesNode:
    """
    Takes a list of tokens, generated by tokens.generate_tokens and puts
    them into a tree structure based on known mutations (a mutation is
    any change to Python that bones knows how to suppress)
    """
    # the root node in a tree
    alpha_mutant = BonesNode(block_type=MODULE, parent=None)
    curr_container = alpha_mutant

    for index, tok in enumerate(tokens):

        # If we find a block_type that bones is interested in (if the block has a mutation
        # that bones knows how to suppress), start a new child node of that block_type and make
        # it the curr_container.
        new_block_type = _is_start_of_block(tok)
        if new_block_type:
            block = BonesNode(block_type=new_block_type, parent=curr_container)
            curr_container.children.append(block)
            curr_container = block

        curr_container.tokens.append(tok)

        if curr_container.is_my_dedent(tok):
            curr_container = curr_container.parent

    return alpha_mutant


def _is_start_of_block(tok):
    if tok.type != NAME:
        return False

    if tok.string == 'class':
        return CLASS

    if tok.string == 'def':
        return FUNCTION

    if tok.string in BDD_BLOCK_TYPES:
        return BDD_BLOCK