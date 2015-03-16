from token import NAME
from bones.block import Block, MODULE, CLASS, FUNCTION, BDD_BLOCK, BDD_BLOCK_TYPES


def parse(tokens):
    module = Block(block_type=MODULE, parent=None)
    curr_container = module

    for index, tok in enumerate(tokens):

        new_block_type = _is_start_of_block(tok)
        if new_block_type:
            block = Block(block_type=new_block_type, parent=curr_container)
            curr_container.children.append(block)
            curr_container = block

        curr_container.tokens.append(tok)

        if curr_container.is_my_dedent(tok):
            curr_container = curr_container.parent

    return module


def _is_start_of_block(tok):
    if tok.type != NAME:
        return False

    if tok.string == 'class':
        return CLASS

    if tok.string == 'def':
        return FUNCTION

    if tok.string in BDD_BLOCK_TYPES:
        return BDD_BLOCK